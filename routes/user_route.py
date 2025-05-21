from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from dependencies import check_role, get_current_user, get_user_service
from models.user import (
    UserCreate,
    UserCreateByAdmin,
    UserPasswordRequest,
    UserPasswordReset,
    UserRead,
    UserUpdate,
    UserUpdateRole,
    UserUpdateStatus,
)
from services import auth_service
from services.user_service import UserService
from utils import mail_sender

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserRead)
async def create(
    user_data: UserCreate, service: UserService = Depends(get_user_service)
):
    user = await service.create_user(user_data)
    token = auth_service.create_verification_token(user.email)
    await mail_sender.send_verification_email(user.email, token)
    return user


@router.post("/create", response_model=UserRead)
async def create_by_admin(
    user_data: UserCreateByAdmin,
    user: UserRead = Depends(check_role("admin")),
    service: UserService = Depends(get_user_service),
):
    user_created = await service.create_user(user_data)
    token = auth_service.create_verification_token(user_created.email)
    await mail_sender.send_verification_email(user_created.email, token)
    return user_created


@router.get("/verify-email", response_model=UserRead)
async def verify_email(token: str, service: UserService = Depends(get_user_service)):
    return await service.verify_email(token)


@router.get("/", response_model=List[UserRead])
async def get_all_users(
    user: UserRead = Depends(check_role("admin")),
    service: UserService = Depends(get_user_service),
):
    return await service.get_all_users()


@router.get("/profile", response_model=UserRead)
async def get_profile(
    user: UserRead = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return await service.get_user_by_id(user.id)


@router.post("/reset-password-confirm", response_model=UserRead)
async def reset_password_confirm(
    token: str,
    passwords: UserPasswordReset,
    service: UserService = Depends(get_user_service),
):
    return await service.reset_password(token, passwords)


@router.post("/reset-password")
async def reset_password(user: UserPasswordRequest):
    token = auth_service.create_verification_token(user.email)
    await mail_sender.send_reset_password_email(user.email, token)
    return {
        "message": "Revisa tu correo y sigue los pasos para recuperar tu contraseña"
    }


@router.patch("/set-photo", response_model=UserRead)
async def set_photo(
    user: UserRead = Depends(get_current_user),
    photo: UploadFile = File(...),
    service: UserService = Depends(get_user_service),
):
    return await service.set_user_photo(user.id, photo)


@router.patch("/unset-photo", response_model=UserRead)
async def set_photo(
    user: UserRead = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return await service.unset_user_photo(user.id)


@router.put("/update-profile", response_model=UserRead)
async def update_profile(
    user_data: UserUpdate,
    user: UserRead = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return await service.update_user(user.id, user_data)


@router.patch("/{user_id}/set-status", response_model=UserRead)
async def set_role(
    user_id: int,
    user_data: UserUpdateStatus,
    user: UserRead = Depends(check_role("admin")),
    service: UserService = Depends(get_user_service),
):
    return await service.update_user(user_id, user_data)


@router.patch("/{user_id}/set-role", response_model=UserRead)
async def set_role(
    user_id: int,
    user_data: UserUpdateRole,
    user: UserRead = Depends(check_role("admin")),
    service: UserService = Depends(get_user_service),
):
    return await service.update_user(user_id, user_data)
