from fastapi import FastAPI
from routers import note

app = FastAPI(title="Simple Notes API")
app.include_router(note.router)
