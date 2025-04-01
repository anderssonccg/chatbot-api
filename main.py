from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.db import init_db
from routes import auth_route, user_route


#@asynccontextmanager
#async def lifespan(app: FastAPI):
#    await init_db()
#    yield
#lifespan=lifespan

app = FastAPI()

app.include_router(user_route.router)
app.include_router(auth_route.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
