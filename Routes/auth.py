from fastapi import APIRouter, Depends

from Utils.dependencies import get_current_user
from Controllers.auth import create_user, authenticate_user, change_password
from Schemas.schemas import PasswordChange, UserCreate, UserResponse, TokenResponse, UserLogin
from Services.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    token = authenticate_user(db, email=credentials.user_email, password=credentials.user_password)

    return {"access_token": token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse)
def register(user_info: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user_info)
    return new_user

@router.post("/change-password")
def update_password(
    passwords: PasswordChange, 
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    updated_user = change_password(db, current_user["user_id"], passwords)
    return {"message": "Password updated successfully"}
