
from sqlalchemy.orm import Session
from Schemas.schemas import UserCreate
from Models.models import User

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