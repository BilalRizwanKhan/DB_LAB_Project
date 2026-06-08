from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
import models, schemas

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/{property_id}")
def add_review(property_id: int, data: schemas.ReviewSchema, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not db.query(models.Property).filter_by(id=property_id).first():
        raise HTTPException(404, "Property not found")
    if not (1 <= data.rating <= 5):
        raise HTTPException(400, "Rating must be between 1 and 5")
    if db.query(models.Review).filter_by(user_id=current_user.id, property_id=property_id).first():
        raise HTTPException(400, "You have already reviewed this property")
    review = models.Review(
        property_id=property_id,
        user_id=current_user.id,
        user_name=current_user.name,
        rating=data.rating,
        comment=data.comment
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

@router.get("/{property_id}")
def get_reviews(property_id: int, db: Session = Depends(get_db)):
    reviews = db.query(models.Review).filter_by(property_id=property_id).all()
    avg = round(sum(r.rating for r in reviews) / len(reviews), 1) if reviews else 0
    return {"average_rating": avg, "total": len(reviews), "reviews": reviews}

@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    review = db.query(models.Review).filter_by(id=review_id).first()
    if not review:
        raise HTTPException(404, "Review not found")
    if review.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(403, "Not authorized")
    db.delete(review)
    db.commit()
    return {"message": "Review deleted"}
