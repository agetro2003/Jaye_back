from fastapi import Header, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from Utils.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token de autorización inválido")
        return {"user_id": user_id, "username": payload.get("username"), "email": payload.get("email")}
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token de autorización expirado")
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token de autorización inválido")
    

def get_token(authorization: str = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token de autorización no proporcionado")
    

    return {"user_id": 1, "username": "jaye"}

    