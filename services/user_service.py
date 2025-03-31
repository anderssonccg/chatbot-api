from typing import List, Optional
from fastapi import HTTPException, status
from models.user import User, UserCreate, UserRead
from repositories.user_repository import UserRepository
from passlib.context import CryptContext

class UserService:

    crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_all_users(self) -> List[UserRead]:
        users = await self.user_repository.get_all()
        return [UserRead.model_validate(user) for user in users]

    async def get_user_by_id(self, user_id: int) -> Optional[UserRead]:
        user = await self.user_repository.get(user_id)
        return UserRead.model_validate(user) if user else None

    async def create_user(self, user_data: UserCreate) -> UserRead:
        user = User.model_validate(user_data.model_dump())
        await self.validate_email(user.email)
        user.password = self.crypt.hash(user.password)
        created_user = await self.user_repository.create(user)
        return UserRead.model_validate(created_user)

    async def update_user(self, user_id: int, user_data: UserCreate) -> Optional[UserRead]:
        updated_user = await self.user_repository.update(user_id, user_data)
        return UserRead.model_validate(updated_user) if updated_user else None

    async def validate_email(self, email: str):
        if not email.endswith(f"@ufps.edu.co"):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="El email no es valido. Debe ser su email institucional")
        email_already_used = await self.user_repository.get_by_email(email)
        if email_already_used:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya se encuenta en uso")

    async def delete_user(self, user_id: int) -> bool:
        return await self.user_repository.delete(user_id)