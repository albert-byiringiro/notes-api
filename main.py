from fastapi import FastAPI
from routers import note

app = FastAPI(title="Notes API", version="0.1.0")

app.include_router(note.router)
