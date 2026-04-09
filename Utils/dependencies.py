from fastapi import Header, HTTPException, Depends

def get_token(authorization: str = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token de autorización no proporcionado")
    

    return {"user_id": 1, "username": "jaye"}

    