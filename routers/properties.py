import os, shutil, uuid
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from auth import get_current_user
import models, schemas

router = APIRouter(prefix="/properties", tags=["Properties"])

UPLOAD_DIR = "uploads"
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}

@router.post("")
def post_property(data: schemas.PropertySchema, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    prop = models.Property(**data.dict(), owner_id=current_user.id)
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return prop

@router.post("/{id}/image")
def upload_image(id: int, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    prop = db.query(models.Property).filter_by(id=id).first()
    if not prop:
        raise HTTPException(404, "Property not found")
    if prop.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(403, "Not authorized")
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, "Only JPEG, PNG and WebP images are allowed")

    # Delete old image if exists
    if prop.image_path and os.path.exists(prop.image_path):
        os.remove(prop.image_path)

    ext      = file.filename.rsplit(".", 1)[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    prop.image_path = filepath
    db.commit()
    return {"message": "Image uploaded", "image_url": f"/uploads/{filename}"}

@router.get("")
def get_properties(
    search:    Optional[str] = Query(None),
    min_price: Optional[int] = Query(None),
    max_price: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Property)
    if search:
        query = query.filter(
            models.Property.title.ilike(f"%{search}%") |
            models.Property.location.ilike(f"%{search}%")
        )
    if min_price is not None:
        query = query.filter(models.Property.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Property.price <= max_price)
    return query.all()

@router.get("/{id}")
def get_property(id: int, db: Session = Depends(get_db)):
    prop = db.query(models.Property).filter_by(id=id).first()
    if not prop:
        raise HTTPException(404, "Property not found")
    return prop

@router.delete("/{id}")
def delete_property(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    prop = db.query(models.Property).filter_by(id=id).first()
    if not prop:
        raise HTTPException(404, "Property not found")
    if prop.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(403, "Not authorized")
    if prop.image_path and os.path.exists(prop.image_path):
        os.remove(prop.image_path)
    db.delete(prop)
    db.commit()
    return {"message": "Property deleted"}
