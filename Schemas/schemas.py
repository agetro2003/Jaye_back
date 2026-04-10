from datetime import datetime

from typing import Optional 
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
    song_abc_text: Optional[str] = ""
    song_songwriter: str
    folder_id: int

class SongResponse(BaseModel):
    song_id: int
    song_title: str
    folder_id: int
    song_abc_text: Optional[str]
    song_last_update: datetime
    song_created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class SongUpdate(BaseModel):
    song_title: Optional[str] = None
    song_abc_text: Optional[str] = None
    song_songwriter: Optional[str] = None
    folder_id: Optional[int] = None

class UserLogin(BaseModel):
    user_email: EmailStr
    user_password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class PasswordChange(BaseModel):
    old_password: str
    new_password: str