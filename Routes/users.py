from fastapi import APIRouter, Depends

from Utils.dependencies import get_token


router = APIRouter(
    prefix="/users", 
    tags=["Users"],
    dependencies=[Depends(get_token)])

@router.get("/me")
def get_current_user():
    return {"mensaje": "Aquí irán los detalles del usuario actual"}