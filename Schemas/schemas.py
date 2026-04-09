from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    user_name: str
    user_email: EmailStr
    user_password: str

class UserResponse(BaseModel):
    user_id: int
    user_name: str
    user_email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class FolderCreate(BaseModel):
    folder_name: str

class FolderResponse(BaseModel):
    folder_id: int
    folder_name: str
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class SongCreate(BaseModel):
    song_title: str
    song_abc_text: str
    song_songwriter: str

class SongResponse(BaseModel):
    song_id: int
    song_title: str
    folder_id: int
    song_abc_text: str
    song_songwriter: str
    song_last_update: datetime
    song_created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)