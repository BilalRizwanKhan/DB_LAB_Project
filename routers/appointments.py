from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
from utils.email import email_appointment_booked
import models, schemas

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/{property_id}")
def book_appointment(property_id: int, data: schemas.AppointmentSchema, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    prop = db.query(models.Property).filter_by(id=property_id).first()
    if not prop:
        raise HTTPException(404, "Property not found")
    if prop.owner_id == current_user.id:
        raise HTTPException(400, "You cannot book a visit to your own property")
    # Prevent duplicate booking on same date/time
    existing = db.query(models.Appointment).filter_by(
        property_id=property_id, user_id=current_user.id,
        visit_date=data.visit_date, visit_time=data.visit_time
    ).first()
    if existing:
        raise HTTPException(400, "You already have an appointment at this date and time")
    appt = models.Appointment(
        property_id=property_id,
        user_id=current_user.id,
        user_name=current_user.name,
        user_email=current_user.email,
        visit_date=data.visit_date,
        visit_time=data.visit_time,
        note=data.note
    )
    db.add(appt)
    db.commit()
    db.refresh(appt)
    # Send confirmation email
    email_appointment_booked(current_user.name, current_user.email, prop.title, data.visit_date, data.visit_time)
    return appt

@router.get("/mine")
def my_appointments(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    appts = db.query(models.Appointment).filter_by(user_id=current_user.id).all()
    result = []
    for a in appts:
        prop = db.query(models.Property).filter_by(id=a.property_id).first()
        result.append({
            "id":             a.id,
            "property_title": prop.title if prop else "Deleted",
            "property_id":    a.property_id,
            "visit_date":     a.visit_date,
            "visit_time":     a.visit_time,
            "note":           a.note,
            "status":         a.status
        })
    return result

@router.get("/received")
def received_appointments(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    my_props = db.query(models.Property).filter_by(owner_id=current_user.id).all()
    prop_ids = [p.id for p in my_props]
    if not prop_ids:
        return []
    appts = db.query(models.Appointment).filter(models.Appointment.property_id.in_(prop_ids)).all()
    result = []
    for a in appts:
        prop = db.query(models.Property).filter_by(id=a.property_id).first()
        result.append({
            "id":             a.id,
            "property_title": prop.title if prop else "Deleted",
            "user_name":      a.user_name,
            "user_email":     a.user_email,
            "visit_date":     a.visit_date,
            "visit_time":     a.visit_time,
            "note":           a.note,
            "status":         a.status
        })
    return result

@router.put("/{appt_id}/confirm")
def confirm_appointment(appt_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    appt = db.query(models.Appointment).filter_by(id=appt_id).first()
    if not appt:
        raise HTTPException(404, "Appointment not found")
    prop = db.query(models.Property).filter_by(id=appt.property_id).first()
    if not prop or (prop.owner_id != current_user.id and not current_user.is_admin):
        raise HTTPException(403, "Not authorized")
    appt.status = "confirmed"
    db.commit()
    return {"message": "Appointment confirmed"}

@router.put("/{appt_id}/cancel")
def cancel_appointment(appt_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    appt = db.query(models.Appointment).filter_by(id=appt_id).first()
    if not appt:
        raise HTTPException(404, "Appointment not found")
    prop = db.query(models.Property).filter_by(id=appt.property_id).first()
    is_owner = prop and prop.owner_id == current_user.id
    is_buyer = appt.user_id == current_user.id
    if not is_owner and not is_buyer and not current_user.is_admin:
        raise HTTPException(403, "Not authorized")
    appt.status = "cancelled"
    db.commit()
    return {"message": "Appointment cancelled"}
