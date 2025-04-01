from fastapi import APIRouter, Depends
from dependencies import get_current_user, get_user_service
from models.user import UserCreate, UserRead
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserRead)
async def create(user_data: UserCreate, service: UserService = Depends(get_user_service)):
    return await service.create_user(user_data)

@router.get("/profile", response_model=UserRead)
async def get_profile(user: UserRead = Depends(get_current_user), service: UserService = Depends(get_user_service)):
    return await service.get_user_by_id(user.id)