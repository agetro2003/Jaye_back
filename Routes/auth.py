from fastapi import APIRouter, Depends

from Utils.dependencies import get_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(credentials: dict):
    return {"mensaje": "Usuario autenticado exitosamente", "credentials": credentials}

@router.post("/register")
def register(user_info: dict):
    return {"mensaje": "Usuario registrado exitosamente", "user_info": user_info}

@router.post("/change-password")
def change_password(password_change: dict, current_user: dict = Depends(get_token)):
    return {"mensaje": "Contraseña cambiada exitosamente", "password_change": password_change}

