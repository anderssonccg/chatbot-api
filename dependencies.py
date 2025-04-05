from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config.db import SessionDep
from models.user import UserRead
from repositories.resource_repository import ResourceRepository
from repositories.user_repository import UserRepository
from services.resource_service import ResourceService
from services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_user_service(session: SessionDep) -> UserService:
    user_repository = UserRepository(session)
    return UserService(user_repository)


def get_auth_service(session: SessionDep) -> UserService:
    user_repository = UserRepository(session)
    return UserService(user_repository)


def get_resource_service(session: SessionDep) -> ResourceService:
    resource_repository = ResourceRepository(session)
    return ResourceService(resource_repository)


def check_role(required_role: str):
    async def role_checker(user: UserRead = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No estas autorizado para realizar esta accion.",
            )
        return user

    return role_checker


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service),
) -> UserRead:
    return await service.get_current_user(token)
