from Models.models import Folder
from sqlalchemy.orm import Session

def get_user_folders(db: Session, user_id: int):
    return db.query(Folder).filter(Folder.user_id == user_id).all()

def get_folder_by_id(db: Session, folder_id: int, user_id: int):
    return db.query(Folder).filter(Folder.folder_id == folder_id, Folder.user_id == user_id).first()

def add_folder(db: Session, new_folder: Folder):
    db.add(new_folder)
    db.commit()
    db.refresh(new_folder)
    return new_folder

def update_folder(db: Session, folder: Folder, folder_data: dict):
    for key, value in folder_data.items():
        setattr(folder, key, value)
    
    db.commit()
    db.refresh(folder)
    return folder

def delete_folder(db: Session, folder: Folder):
    db.delete(folder)
    db.commit()
    return folder

