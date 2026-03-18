from fastapi import FastAPI

app = FastAPI(title="Simple Notes API")


@app.get("/")
async def get_all():
    return "Hello, World"
