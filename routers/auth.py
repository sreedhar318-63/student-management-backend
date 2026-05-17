from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models.user import User
from utils.hashing import hash_password, verify_password
from utils.jwt import create_access_token

from utils.email import generate_otp, send_otp_email, otp_store

from typing import Optional

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None
    password: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    email: str
    otp: str
    new_password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

@router.post("/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Check if email exists (only if email is provided)
    if user.email:
        existing_email = db.query(User).filter(User.email == user.email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        role="user"
    )
    db.add(new_user)
    db.commit()
    return {"message": f"Account created for {user.username}"}

@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    found = db.query(User).filter(User.username == user.username).first()
    if not found or not verify_password(user.password, found.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": create_access_token(found.username),
        "token_type": "bearer",
        "role": found.role
    }

@router.post("/forgot-password")
def forgot_password(req: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with this email not found")
    
    otp = generate_otp()
    otp_store[req.email] = otp
    send_otp_email(req.email, otp)
    
    return {"message": "OTP sent to your email"}

@router.post("/reset-password")
def reset_password(req: ResetPasswordRequest, db: Session = Depends(get_db)):
    if req.email not in otp_store or otp_store[req.email] != req.otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.hashed_password = hash_password(req.new_password)
    db.commit()
    
    # Remove OTP after use
    del otp_store[req.email]
    
    return {"message": "Password reset successfully"}