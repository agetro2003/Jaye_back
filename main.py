from fastapi import FastAPI

from Routes import songs, folders, users, auth

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Jaye"}

app.include_router(songs.router)
app.include_router(folders.router)
app.include_router(users.router)
app.include_router(auth.router)


