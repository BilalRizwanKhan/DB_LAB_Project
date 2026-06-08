from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import get_db
from auth import create_token
from utils.email import email_welcome
import models, schemas

router = APIRouter(prefix="/auth", tags=["Auth"])
pwd = CryptContext(schemes=["bcrypt"])

@router.post("/signup")
def signup(data: schemas.SignupSchema, db: Session = Depends(get_db)):
    if db.query(models.User).filter_by(email=data.email).first():
        raise HTTPException(400, "Email already registered")
    user = models.User(name=data.name, email=data.email, password=pwd.hash(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    # Send welcome email
    email_welcome(user.name, user.email)
    return {"message": "Account created successfully"}

@router.post("/login", response_model=schemas.TokenSchema)
def login(data: schemas.LoginSchema, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=data.email).first()
    if not user or not pwd.verify(data.password, user.password):
        raise HTTPException(401, "Invalid email or password")
    token = create_token({"id": user.id, "email": user.email, "is_admin": user.is_admin})
    return {"access_token": token, "token_type": "bearer", "name": user.name}
