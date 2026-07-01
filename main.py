from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Routes import songs, folders, users, auth
from Services.database import engine
from Models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Jaye API",
    description="API para la plataforma web de composición musical asistida por IA",
    version="1.0.0"
)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "*"
    # Puedes añadir "*" temporalmente si te da problemas, pero esto es más seguro
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Esto permite el OPTIONS, POST, GET, etc.
    allow_headers=["*"], # Permite enviar tokens y JSON
)

@app.get("/")
def read_root():
    return {"Hello": "Jaye"}

app.include_router(songs.router)
app.include_router(folders.router)
app.include_router(users.router)
app.include_router(auth.router)


