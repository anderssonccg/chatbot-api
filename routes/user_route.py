from fastapi import APIRouter, Depends
from models.user import UserCreate, UserRead
from config.db import SessionDep
from repositories.user_repository import UserRepository
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

def get_user_service(session: SessionDep) -> UserService:
    user_repository = UserRepository(session)
    return UserService(user_repository)

@router.post("/register", response_model=UserRead)
async def create(user_data: UserCreate, service: UserService = Depends(get_user_service)):
    return await service.create_user(user_data)
