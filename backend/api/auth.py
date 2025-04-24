# backend/api/auth.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.user import User
from auth.jwt_handler import create_access_token
from auth.password_utils import hash_password, verify_password
from auth.dependencies import get_current_user

router = APIRouter()

# Pydantic models
class UserSignup(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Signup route
@router.post("/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(400, "Email already registered")

    hashed = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"user_id": str(new_user.id)})
    return {"access_token": token, "token_type": "bearer"}

# Login route
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    user_in_db = db.query(User).filter(User.email == user.email).first()
    if not user_in_db or not verify_password(user.password, user_in_db.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({"user_id": str(user_in_db.id)})
    return {"access_token": token, "token_type": "bearer"}

# 👇 Add this route at the bottom
@router.get("/me")
def read_profile(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role
    }
