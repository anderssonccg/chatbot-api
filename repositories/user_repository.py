from typing import List, Optional
from sqlmodel import select
from config.db import SessionDep
from models.user import User
from repositories.repository_interface import IRepository


class UserRepository(IRepository[User]):

    def __init__(self, session: SessionDep):
        self.session = session

    async def get_all(self) -> List[User]:
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get(self, id: int) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.id == id))
        return result.scalars().first()

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, id: int, user_data: User) -> Optional[User]:
        user = await self.get(id)
        if user:
            user.sqlmodel_update(user_data)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        return None

    async def delete(self, id: int) -> bool:
        user = await self.get(id)
        if user:
            await self.session.delete(user)
            await self.session.commit()
            return True
        return False
