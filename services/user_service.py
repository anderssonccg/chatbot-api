import os
from typing import List, Optional
from fastapi import HTTPException, UploadFile, status
from passlib.context import CryptContext
from models.user import User, UserCreate, UserPasswordReset, UserRead, UserUpdate
from repositories.user_repository import UserRepository
from services import auth_service
from utils import gcs

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_all_users(self) -> List[UserRead]:
        users = await self.user_repository.get_all()
        return [UserRead.model_validate(user) for user in users]

    async def get_user_by_id(self, user_id: int) -> Optional[UserRead]:
        user = await self.user_repository.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario inexistente."
            )
        return UserRead.model_validate(user)

    async def create_user(self, user_data: UserCreate) -> UserRead:
        user = User.model_validate(user_data.model_dump())
        await self.validate_email(user.email)
        user.password = crypt.hash(user.password)
        created_user = await self.user_repository.create(user)
        return UserRead.model_validate(created_user)

    async def auth_user(self, username: str, password: str) -> UserRead:
        user = await self.user_repository.get_by_email(username)
        if not user or not crypt.verify(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return UserRead.model_validate(user)

    async def get_current_user(self, token: str):
        id = auth_service.decode_token(token)
        if id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido."
            )
        user = await self.get_user_by_id(int(id))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario inexistente."
            )
        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Debes verificar tu correo para acceder completamente.",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El usuario se encuentra inactivo. Contacte con el administrador",
            )
        return UserRead.model_validate(user)

    async def get_by_email(self, email: str) -> Optional[UserRead]:
        return await self.user_repository.get_by_email(email)

    async def verify_email(self, token: str) -> Optional[UserRead]:
        email = auth_service.decode_verification_token(token)
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token inválido o expirado",
            )
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario inexistente"
            )
        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Su correo ya se ha verificado",
            )
        user.is_verified = True
        return await self.user_repository.update(user.id, user)

    async def reset_password(self, token: str, passwords: UserPasswordReset):
        if passwords.password != passwords.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Las contraseñas no son iguales",
            )
        email = auth_service.decode_verification_token(token)
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token inválido o expirado",
            )
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario inexistente"
            )
        user.password = crypt.hash(passwords.confirm_password)
        return await self.user_repository.update(user.id, user)

    async def update_user(self, user_id: int, user_data) -> Optional[UserRead]:
        user = await self.user_repository.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario inexsistente."
            )
        updated_user = await self.user_repository.update(user_id, user_data)
        return UserRead.model_validate(updated_user)

    async def validate_email(self, email: str):
        if not email.endswith(f"@ufps.edu.co"):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El email no es valido. Debe ser su email institucional",
            )
        email_already_used = await self.user_repository.get_by_email(email)
        if email_already_used:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El email ya se encuenta en uso",
            )

    async def set_user_photo(self, user_id: int, photo: UploadFile) -> UserRead:
        user = await self.user_repository.get(user_id)
        self.validate_photo_extension(photo.filename)
        self.delete_photo(user.photo)
        photo_url = gcs.upload_file(photo)["url"]
        user.photo = photo_url
        user_updated = await self.user_repository.update(user.id, user)
        return UserRead.model_validate(user_updated)

    async def unset_user_photo(self, user_id: int) -> UserRead:
        user = await self.user_repository.get(user_id)
        self.delete_photo(user.photo)
        user.photo = None
        user_updated = await self.user_repository.update(user.id, user)
        return UserRead.model_validate(user_updated)

    def delete_photo(self, photo_url: str):
        if photo_url:
            last_photo = photo_url.split("/")[-1]
            gcs.delete_file(last_photo)

    def validate_photo_extension(self, filename: str):
        ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
        ext = os.path.splitext(filename)[1].lower().replace(".", "")
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Formato de imagen no permitido. Solo se aceptan: {', '.join(ALLOWED_EXTENSIONS)}",
            )

    async def delete_user(self, user_id: int) -> bool:
        return await self.user_repository.delete(user_id)
