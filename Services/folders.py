from sqlalchemy import func
from Models.models import Folder, Song
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



def get_user_folders_with_counts(db: Session, user_id: int):
    # 1. Hacemos la consulta cruzando Folder y Song
    results = db.query(
        Folder, 
        func.count(Song.song_id).label('song_count')
    ).outerjoin(
        Song, Folder.folder_id == Song.folder_id
    ).filter(
        Folder.user_id == user_id
    ).group_by(
        Folder.folder_id
    ).all()

    # 2. SQLAlchemy nos devuelve una lista de tuplas: [(Folder_obj, 5), (Folder_obj, 2)]
    # Lo empaquetamos en diccionarios para que FastAPI/Pydantic lo lea perfecto:
    folders_list = []
    for folder, count in results:
        folder_dict = {
            "folder_id": folder.folder_id,
            "folder_name": folder.folder_name,
            "user_id": folder.user_id,
            "song_count": count
        }
        folders_list.append(folder_dict)

    return folders_list