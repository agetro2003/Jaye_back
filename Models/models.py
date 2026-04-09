
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from Utils.database import Base


class User(Base): 
    __tablename__ = "user"
    
    user_id = Column(Integer, primary_key=True, index=True) 
    user_name = Column(String, unique=True, index=True, nullable=False) 
    user_email = Column(String, unique=True, index=True, nullable=False) 
    user_password = Column(String, nullable=False) 

    folders = relationship("Folder", back_populates="owner")


class Folder(Base):
    __tablename__ = "folder"
    
    folder_id = Column(Integer, primary_key=True, index=True) 
    folder_name = Column(String, index=True, nullable=False) 
    user_id = Column(Integer, ForeignKey("user.user_id")) 

    owner = relationship("User", back_populates="folders")
    songs = relationship("Song", back_populates="folder")

class Song(Base):
    __tablename__ = "song"
    
    song_id = Column(Integer, primary_key=True, index=True) 
    song_title = Column(String, index=True, nullable=False) 
    folder_id = Column(Integer, ForeignKey("folder.folder_id"))
    song_abc_text = Column(String)
    song_songwriter = Column(String, nullable=False)
    song_last_update = Column(DateTime, server_default=func.now(), onupdate=func.now())
    song_created_at = Column(DateTime, server_default=func.now())    

    folder = relationship("Folder", back_populates="songs")


