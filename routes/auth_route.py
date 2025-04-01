from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from services.user_service import UserService
from services import auth_service
from config.db import SessionDep
from repositories.user_repository import UserRepository

router = APIRouter(prefix="/auth", tags=["auth"])

def get_auth_service(session: SessionDep) -> UserService:
    user_repository = UserRepository(session)
    return UserService(user_repository)

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), service: UserService = Depends(get_auth_service)):
    user = await service.auth_user(form.username, form.password)
    return auth_service.create_access_token(str(user.id))