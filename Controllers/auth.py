from passlib.context import CryptContext
from Services.auth import get_user, register_user
from fastapi import HTTPException
from Schemas.schemas import PasswordChange, UserCreate
from sqlalchemy.orm import Session
from Models.models import User
from Utils.security import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: UserCreate):
    
    #Check if user already exists
    existing_user = get_user(db, email=user.user_email, username=user.user_name)

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    #Hash the password
    hashed_password = pwd_context.hash(user.user_password)

    #Create new user
    new_user = User(
        user_name=user.user_name,
        user_email=user.user_email,
        user_password=hashed_password
    )
    return register_user(db, new_user)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db, email=email)
    if not user or not verify_password(password, user.user_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token_data = {
        "sub": str(user.user_id),
        "username": user.user_name,
        "email": user.user_email
    }

    token = create_access_token(token_data)
    
    return token

def change_password(db: Session, user_id: int, passwords: PasswordChange):
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(passwords.old_password, user.user_password):
        raise HTTPException(status_code=401, detail="Current password is incorrect")
    hashed_password = pwd_context.hash(passwords.new_password)
    user.user_password = hashed_password
    db.commit()
    db.refresh(user)
    return user