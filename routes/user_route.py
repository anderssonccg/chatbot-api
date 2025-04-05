from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_current_user, get_user_service
from models.user import UserCreate, UserPasswordRequest, UserPasswordReset, UserRead
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


@router.get("/verify-email", response_model=UserRead)
async def verify_email(token: str, service: UserService = Depends(get_user_service)):
    return await service.verify_email(token)


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


# arreglar en modelo, agregar la foto
# update profile
# update foto (gcs)

# del admin -> habilitar o deshabilitar
# cambiar rol
