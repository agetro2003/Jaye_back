

from sqlalchemy.orm import Session
from Services.folders import get_user_folders, add_folder, update_folder, delete_folder, get_folder_by_id
from Models.models import Folder

def users_folders(db: Session, user_id: int):
    return get_user_folders(db, user_id)

def create_folder(db: Session, folder_name: str, user_id: int):
    new_folder = Folder(folder_name=folder_name, user_id=user_id)
    return add_folder(db, new_folder)

def edit_folder(db: Session, folder_id: int, user_id: int, folder_data: dict):
    folder = get_folder_by_id(db, folder_id, user_id)
    if not folder:
        return None
    return update_folder(db, folder, folder_data)

def remove_folder(db: Session, folder_id: int, user_id: int):
    folder = get_folder_by_id(db, folder_id, user_id)
    if not folder:
        return None
    return delete_folder(db, folder)

def get_songs_in_folder(db: Session, folder_id: int, user_id: int):
    folder = get_folder_by_id(db, folder_id, user_id)
    if not folder:
        return None
    return folder.songs


