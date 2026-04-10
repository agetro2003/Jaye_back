from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Services.database import get_db
from Utils.dependencies import get_current_user
from Schemas.schemas import FolderResponse, FolderCreate, SongResponse
from typing import List
from Controllers.folders import users_folders, create_folder, edit_folder, remove_folder, get_songs_in_folder

router = APIRouter(
    prefix="/folders",
    tags=["Folders"],
    dependencies=[Depends(get_current_user)]
    )

@router.get("/", response_model=List[FolderResponse])
def get_folders(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    folders = users_folders(db, current_user["user_id"])
    return folders

@router.post("/", response_model=FolderResponse)
def post_folder(
    folder: FolderCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_folder(db, folder.folder_name, current_user["user_id"])

@router.put("/{folder_id}", response_model=FolderResponse)
def update_folder(
    folder_id: int, 
    folder: FolderCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_folder = edit_folder(db, folder_id, current_user["user_id"], folder.dict())
    if not updated_folder:
        raise HTTPException(status_code=404, detail="Carpeta no encontrada o no pertenece al usuario")
    return updated_folder


@router.delete("/{folder_id}")
def delete_folder(
    folder_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    deleted_folder = remove_folder(db, folder_id, current_user["user_id"])
    if not deleted_folder:
        raise HTTPException(status_code=404, detail="Carpeta no encontrada o no pertenece al usuario")
    return {"message": "Carpeta eliminada exitosamente"}

@router.get("/{folder_id}/songs", response_model=List[SongResponse])   
def song_in_folder(
    folder_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    songs = get_songs_in_folder(db, folder_id, current_user["user_id"])
    if songs is None:
        raise HTTPException(status_code=404, detail="Carpeta no encontrada o no pertenece al usuario")
    return songs