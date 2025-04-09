from fastapi import FastAPI
from routes import auth_route, category_route, faq_route, resource_route, user_route

app = FastAPI()

app.include_router(user_route.router)
app.include_router(auth_route.router)
app.include_router(resource_route.router)
app.include_router(category_route.router)
app.include_router(faq_route.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
