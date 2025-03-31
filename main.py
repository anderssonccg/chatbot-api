from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.db import init_db
from models.user import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}
