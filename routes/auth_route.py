from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import get_user_service
from services.user_service import UserService
from utils import auth
from config.db import SessionDep
from repositories.user_repository import UserRepository

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
):
    user = await service.auth_user(form.username, form.password)
    return auth.create_access_token(str(user.id))
