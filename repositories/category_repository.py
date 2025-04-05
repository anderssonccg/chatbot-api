from typing import List, Optional
from sqlmodel import select
from config.db import SessionDep
from models.category import Category
from repositories.repository_interface import IRepository


class CategoryRepository(IRepository[Category]):

    def __init__(self, session: SessionDep):
        self.session = session

    async def get_all(self) -> List[Category]:
        result = await self.session.execute(select(Category))
        return result.scalars().all()

    async def get(self, id: int) -> Optional[Category]:
        result = await self.session.execute(select(Category).where(Category.id == id))
        return result.scalars().first()

    async def create(self, user: Category) -> Category:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, id: int, user_data: Category) -> Optional[Category]:
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
