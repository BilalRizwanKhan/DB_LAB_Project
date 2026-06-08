from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
import models

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.post("/{property_id}")
def add_favorite(property_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not db.query(models.Property).filter_by(id=property_id).first():
        raise HTTPException(404, "Property not found")
    exists = db.query(models.Favorite).filter_by(user_id=current_user.id, property_id=property_id).first()
    if exists:
        raise HTTPException(400, "Already in favorites")
    db.add(models.Favorite(user_id=current_user.id, property_id=property_id))
    db.commit()
    return {"message": "Added to favorites"}

@router.delete("/{property_id}")
def remove_favorite(property_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    fav = db.query(models.Favorite).filter_by(user_id=current_user.id, property_id=property_id).first()
    if not fav:
        raise HTTPException(404, "Not in favorites")
    db.delete(fav)
    db.commit()
    return {"message": "Removed from favorites"}

@router.get("")
def get_favorites(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    favs = db.query(models.Favorite).filter_by(user_id=current_user.id).all()
    property_ids = [f.property_id for f in favs]
    if not property_ids:
        return []
    return db.query(models.Property).filter(models.Property.id.in_(property_ids)).all()
