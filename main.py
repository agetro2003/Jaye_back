from fastapi import FastAPI

from Routes import songs, folders, users, auth
from Services.database import engine
from Models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Jaye API",
    description="API para la plataforma web de composición musical asistida por IA",
    version="1.0.0"
)


@app.get("/")
def read_root():
    return {"Hello": "Jaye"}

app.include_router(songs.router)
app.include_router(folders.router)
app.include_router(users.router)
app.include_router(auth.router)


