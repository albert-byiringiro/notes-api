from fastapi import FastAPI
from routers import notes

app = FastAPI(title="Simple Notes API")
app.include_router(notes.router)
