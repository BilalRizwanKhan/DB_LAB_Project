import os, shutil, uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import get_db
from auth import get_current_user
import models, schemas

router = APIRouter(prefix="/users", tags=["Users"])
pwd    = CryptContext(schemes=["bcrypt"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
AVATAR_DIR    = "uploads/avatars"
os.makedirs(AVATAR_DIR, exist_ok=True)

@router.get("/me")
def get_profile(current_user: models.User = Depends(get_current_user)):
    return {
        "id":       current_user.id,
        "name":     current_user.name,
        "email":    current_user.email,
        "phone":    current_user.phone,
        "city":     current_user.city,
        "bio":      current_user.bio,
        "avatar":   current_user.avatar,
        "is_admin": current_user.is_admin
    }

@router.put("/me")
def update_profile(data: schemas.ProfileUpdateSchema, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    current_user.name  = data.name
    current_user.phone = data.phone
    current_user.city  = data.city
    current_user.bio   = data.bio
    db.commit()
    return {"message": "Profile updated"}

@router.post("/me/avatar")
def upload_avatar(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, "Only JPEG, PNG and WebP images allowed")
    # Delete old avatar
    if current_user.avatar:
        old_path = current_user.avatar.lstrip("/")
        if os.path.exists(old_path):
            os.remove(old_path)
    ext      = file.filename.rsplit(".", 1)[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(AVATAR_DIR, filename)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    current_user.avatar = f"/uploads/avatars/{filename}"
    db.commit()
    return {"message": "Avatar uploaded", "avatar_url": current_user.avatar}

@router.put("/me/password")
def change_password(data: schemas.PasswordChangeSchema, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not pwd.verify(data.current_password, current_user.password):
        raise HTTPException(400, "Current password is incorrect")
    current_user.password = pwd.hash(data.new_password)
    db.commit()
    return {"message": "Password changed successfully"}

@router.get("/me/listings")
def my_listings(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Property).filter_by(owner_id=current_user.id).all()

@router.delete("/me/listings/{property_id}")
def delete_my_listing(property_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    prop = db.query(models.Property).filter_by(id=property_id, owner_id=current_user.id).first()
    if not prop:
        raise HTTPException(404, "Property not found or not yours")
    if prop.image_path and os.path.exists(prop.image_path):
        os.remove(prop.image_path)
    db.delete(prop)
    db.commit()
    return {"message": "Listing deleted"}
