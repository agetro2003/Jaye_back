from Models.models import Folder, Song
from sqlalchemy.orm import Session

def get_songs_from_folder(db: Session, folder_id: int):
    return db.query(Song).filter(Song.folder_id == folder_id).all()

def add_song(db: Session, new_song: Song):
    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song

def update_song(db: Session, song: Song, song_data: dict):
    for key, value in song_data.items():
        setattr(song, key, value)
    
    db.commit()
    db.refresh(song)
    return song

def delete_song(db: Session, song: Song):
    db.delete(song)
    db.commit()
    return song

def get_song_by_id(db: Session, song_id: int, user_id: int):
    return db.query(Song).join(Folder).filter(
        Song.song_id == song_id,
        Folder.user_id == user_id
        ).first()