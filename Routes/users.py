from fastapi import APIRouter, Depends

from Utils.dependencies import get_current_user


router = APIRouter(
    prefix="/users", 
    tags=["Users"],
    dependencies=[Depends(get_current_user)])

@router.get("/me")
def get_user_data(current_user: dict = Depends(get_current_user)):
    return current_user