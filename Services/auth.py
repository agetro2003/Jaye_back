import uuid
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from Schemas.schemas import UserCreate
from Models.models import User, PasswordResetToken
from typing import Optional
#Find user by email or username
def get_user(db: Session, email: str = None, username: str = None, user_id: int = None):
    if email:
        return db.query(User).filter(User.user_email == email).first()
    if username:
        return db.query(User).filter(User.user_name == username).first()
    if user_id:
        return db.query(User).filter(User.user_id == user_id).first()
    return None

def register_user(db: Session, new_user: User):
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



RESET_TOKEN_EXPIRE_MINUTES = 15

def create_reset_token(db: Session, user_id: int) -> PasswordResetToken:
    """
    Invalida cualquier token anterior sin usar de este usuario y crea uno nuevo.
    Esto evita que queden varios enlaces "vivos" si el usuario pide el correo
    de recuperación más de una vez.
    """
    db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user_id,
        PasswordResetToken.used == False
    ).update({"used": True})

    reset_token = PasswordResetToken(
        token=str(uuid.uuid4()),
        user_id=user_id,
        expires_at=datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    )
    db.add(reset_token)
    db.commit()
    db.refresh(reset_token)
    return reset_token

def get_valid_reset_token(db: Session, token: str) -> Optional[PasswordResetToken]:   
    """
    Devuelve el token solo si existe, no ha sido usado y no ha expirado.
    """
    reset_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == token
    ).first()

    if not reset_token:
        return None
    if reset_token.used:
        return None
    if reset_token.expires_at < datetime.utcnow():
        return None

    return reset_token