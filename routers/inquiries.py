from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
from utils.email import email_inquiry_received, email_inquiry_replied
import models, schemas

router = APIRouter(prefix="/inquiries", tags=["Inquiries"])

@router.post("/{property_id}")
def send_inquiry(property_id: int, data: schemas.InquirySchema, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    prop = db.query(models.Property).filter_by(id=property_id).first()
    if not prop:
        raise HTTPException(404, "Property not found")
    if prop.owner_id == current_user.id:
        raise HTTPException(400, "You cannot inquire about your own property")
    inquiry = models.Inquiry(
        property_id=property_id,
        buyer_id=current_user.id,
        buyer_name=current_user.name,
        buyer_email=current_user.email,
        message=data.message
    )
    db.add(inquiry)
    db.commit()
    db.refresh(inquiry)
    # Notify seller
    seller = db.query(models.User).filter_by(id=prop.owner_id).first()
    if seller:
        email_inquiry_received(seller.name, seller.email, current_user.name, prop.title)
    return inquiry

@router.get("/mine")
def my_inquiries(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    inquiries = db.query(models.Inquiry).filter_by(buyer_id=current_user.id).all()
    result = []
    for inq in inquiries:
        prop = db.query(models.Property).filter_by(id=inq.property_id).first()
        result.append({
            "id": inq.id,
            "property_title": prop.title if prop else "Deleted",
            "message": inq.message,
            "status": inq.status,
            "reply": inq.reply
        })
    return result

@router.get("/received")
def received_inquiries(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    my_props = db.query(models.Property).filter_by(owner_id=current_user.id).all()
    prop_ids = [p.id for p in my_props]
    if not prop_ids:
        return []
    inquiries = db.query(models.Inquiry).filter(models.Inquiry.property_id.in_(prop_ids)).all()
    result = []
    for inq in inquiries:
        prop = db.query(models.Property).filter_by(id=inq.property_id).first()
        result.append({
            "id": inq.id,
            "property_title": prop.title if prop else "Deleted",
            "buyer_name": inq.buyer_name,
            "buyer_email": inq.buyer_email,
            "message": inq.message,
            "status": inq.status,
            "reply": inq.reply
        })
    return result

@router.put("/{inquiry_id}/reply")
def reply_inquiry(inquiry_id: int, data: schemas.InquiryReplySchema, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    inq  = db.query(models.Inquiry).filter_by(id=inquiry_id).first()
    if not inq:
        raise HTTPException(404, "Inquiry not found")
    prop = db.query(models.Property).filter_by(id=inq.property_id).first()
    if not prop or (prop.owner_id != current_user.id and not current_user.is_admin):
        raise HTTPException(403, "Not authorized")
    inq.reply  = data.reply
    inq.status = "replied"
    db.commit()
    # Notify buyer
    email_inquiry_replied(inq.buyer_name, inq.buyer_email, prop.title)
    return {"message": "Reply sent"}

@router.put("/{inquiry_id}/close")
def close_inquiry(inquiry_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    inq = db.query(models.Inquiry).filter_by(id=inquiry_id).first()
    if not inq:
        raise HTTPException(404, "Inquiry not found")
    if inq.buyer_id != current_user.id and not current_user.is_admin:
        raise HTTPException(403, "Not authorized")
    inq.status = "closed"
    db.commit()
    return {"message": "Inquiry closed"}
