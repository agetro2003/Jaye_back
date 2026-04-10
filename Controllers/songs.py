from Services.songs import get_song_by_id, get_songs_from_folder, update_song, delete_song, add_song
from Services.folders import get_folder_by_id
from Models.models import Song
from sqlalchemy.orm import Session

def songs_in_folder(db: Session, folder_id: int, user_id: int):
    folder = get_folder_by_id(db, folder_id, user_id)
    if not folder:
        return None
    return get_songs_from_folder(db, folder_id)

def create_song(db: Session, song_title: str, song_songwriter: str, folder_id: int, user_id: int):

    db_folder = get_folder_by_id(db, folder_id, user_id)
    if not db_folder:
        return None
    
    new_song = Song(song_title=song_title, song_songwriter=song_songwriter, folder_id=folder_id)
    return add_song(db, new_song)

def edit_song(db: Session, song_id: int, song_data: dict, user_id: int):
    song = get_song(db, song_id, user_id)
    if not song:
        return None

    #Evitar que el usuario mueva la canción a una carpeta que no le pertenece
    if "folder_id" in song_data and song_data["folder_id"] != song.folder_id:
        new_folder = get_folder_by_id(db, song_data["folder_id"], user_id)
        if not new_folder:
            return None

    
    return update_song(db, song, song_data)

def remove_song(db: Session, song_id: int, user_id: int):
    song = get_song(db, song_id, user_id)
    if not song:
        return None
    return delete_song(db, song)

def get_song(db: Session, song_id: int, user_id: int):
    song = get_song_by_id(db, song_id, user_id)
    if not song:
        return None
    return song
