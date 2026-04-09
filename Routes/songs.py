from fastapi import APIRouter, Depends

from Utils.dependencies import get_token


router = APIRouter(
    prefix="/songs", 
    tags=["Songs"],
    dependencies=[Depends(get_token)])

@router.get("/{song_id}")
def get_song(song_id: int):
    return {"mensaje": f"Aquí irán los detalles de la canción con ID {song_id}"}

@router.post("/")
def create_song(song: dict):
    return {"mensaje": "Canción creada exitosamente", "song": song}

@router.put("/{song_id}")
def update_song(song_id: int, song: dict):
    return {"mensaje": f"Canción con ID {song_id} actualizada exitosamente", "song": song}

@router.delete("/{song_id}")
def delete_song(song_id: int):
    return {"mensaje": f"Canción con ID {song_id} eliminada exitosamente"}

@router.post("/generate-ai")
def generate_ai_proposal():
    return {"mensaje": "Propuesta de canción generada por IA", "song": {"title": "Nueva Canción", "artist": "IA"}}
