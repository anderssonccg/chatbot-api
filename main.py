from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.db import init_db
from models.user import User
from routes import user_route


#@asynccontextmanager
#async def lifespan(app: FastAPI):
#    await init_db()
#    yield
#lifespan=lifespan

app = FastAPI()

app.include_router(user_route.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
