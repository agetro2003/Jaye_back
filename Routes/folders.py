from fastapi import APIRouter, Depends

from Utils.dependencies import get_token

router = APIRouter(
    prefix="/folders",
    tags=["Folders"],
    dependencies=[Depends(get_token)]
    )

@router.get("/")
def get_folders():
    return {"mensaje": "Aquí irán los detalles de las carpetas"}

@router.post("/")
def create_folder(folder: dict):
    return {"mensaje": "Carpeta creada exitosamente", "folder": folder}

@router.put("/{folder_id}")
def update_folder(folder_id: int, folder: dict):
    return {"mensaje": f"Carpeta con ID {folder_id} actualizada exitosamente", "folder": folder}

@router.delete("/{folder_id}")
def delete_folder(folder_id: int):
    return {"mensaje": f"Carpeta con ID {folder_id} eliminada exitosamente"}

@router.get("/{folder_id}/songs")   
def get_songs_in_folder(folder_id: int):
    return {"mensaje": f"Aquí irán las canciones dentro de la carpeta con ID {folder_id}"}
