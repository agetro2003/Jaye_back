from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Services.database import get_db
from Utils.dependencies import get_current_user
from Controllers.songs import get_recent_songs, songs_in_folder, create_song, edit_song, remove_song, get_song

from AICore.model import generate_proposals

from Schemas.schemas import ProposalRequest, SongCreate, SongResponse, SongUpdate
from typing import List

router = APIRouter(
    prefix="/songs", 
    tags=["Songs"],
    dependencies=[Depends(get_current_user)])

@router.get("/recent", response_model=List[SongResponse])
def get_recent_songs_route(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 5
):
    songs = get_recent_songs(db, current_user["user_id"], limit)
    return songs


@router.get("/{song_id}", response_model=SongResponse)
def get_song_by_id_route(
    song_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    song = get_song(db, song_id, current_user["user_id"])
    if not song:
        raise HTTPException(status_code=404, detail="Canción no encontrada o no pertenece al usuario")
    return song


@router.post("/", response_model=SongResponse)
def post_song(song: SongCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    new_song = create_song(db, song.song_title, song.song_songwriter, song.folder_id, current_user["user_id"])
    if not new_song:
        raise HTTPException(status_code=400, detail="Error al crear la canción. Asegúrate de que la carpeta exista y te pertenezca.")   
    return new_song


@router.put("/{song_id}", response_model=SongResponse)
def put_song(song_id: int, song: SongUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
   
    song_data_dict = song.model_dump(exclude_unset=True)
    updated_song = edit_song(db, song_id, song_data_dict, current_user["user_id"])
    if not updated_song:
        raise HTTPException(status_code=400, detail="Error al actualizar la canción")
    return updated_song

@router.delete("/{song_id}")
def delete_song(song_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    deleted_song = remove_song(db, song_id, current_user["user_id"])
    if not deleted_song:
        raise HTTPException(status_code=400, detail="Error al eliminar la canción")
    return {"mensaje": f"Canción con ID {song_id} eliminada exitosamente"}

@router.post("/generate-ai")
def generate_ai_proposal(
    request: ProposalRequest,
    current_user: dict = Depends(get_current_user)
):
    try: 
        proposals = generate_proposals(
            abc_text=request.abcText,
            bars=request.bars,
            num_variations=request.num_variations,
            temperature=request.temperature
        )
        return {"proposals": proposals}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar propuestas: {str(e)}")
        

