from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.db import init_db
from routes import auth_route, category_route, resource_route, user_route
from models import category, resource, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_route.router)
app.include_router(auth_route.router)
app.include_router(resource_route.router)
app.include_router(category_route.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
