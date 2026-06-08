from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_admin_user
import models

router = APIRouter(prefix="/admin", tags=["Admin"])

# --- Users ---
@router.get("/users")
def get_all_users(db: Session = Depends(get_db), _=Depends(get_admin_user)):
    users = db.query(models.User).all()
    return [{"id": u.id, "name": u.name, "email": u.email, "is_admin": u.is_admin} for u in users]

@router.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db), current=Depends(get_admin_user)):
    user = db.query(models.User).filter_by(id=id).first()
    if not user:
        raise HTTPException(404, "User not found")
    if user.id == current.id:
        raise HTTPException(400, "Cannot delete yourself")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

@router.put("/users/{id}/make-admin")
def make_admin(id: int, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    user = db.query(models.User).filter_by(id=id).first()
    if not user:
        raise HTTPException(404, "User not found")
    user.is_admin = True
    db.commit()
    return {"message": f"{user.name} is now an admin"}

# --- Properties ---
@router.get("/properties")
def get_all_properties(db: Session = Depends(get_db), _=Depends(get_admin_user)):
    return db.query(models.Property).all()

@router.delete("/properties/{id}")
def delete_property(id: int, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    prop = db.query(models.Property).filter_by(id=id).first()
    if not prop:
        raise HTTPException(404, "Property not found")
    db.delete(prop)
    db.commit()
    return {"message": "Property deleted"}

# --- Stats ---
@router.get("/stats")
def get_stats(db: Session = Depends(get_db), _=Depends(get_admin_user)):
    return {
        "total_users":      db.query(models.User).count(),
        "total_properties": db.query(models.Property).count(),
        "total_admins":     db.query(models.User).filter_by(is_admin=True).count(),
    }
