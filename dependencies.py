from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from config.db import SessionDep
from models.user import UserRead
from repositories.user_repository import UserRepository
from services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_user_service(session: SessionDep) -> UserService:
    user_repository = UserRepository(session)
    return UserService(user_repository)

async def get_current_user(token: str = Depends(oauth2_scheme), service: UserService = Depends(get_user_service)) -> UserRead:
    return await service.get_current_user(token)
    