from typing import List, Optional
from sqlmodel import select
from sqlalchemy.orm import selectinload
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

    async def get_with_resources(self, id: int) -> Optional[Category]:
        result = await self.session.execute(
            select(Category)
            .where(Category.id == id)
            .options(selectinload(Category.resources))
        )
        return result.scalars().first()

    async def get_by_name(self, name: str) -> Optional[Category]:
        result = await self.session.execute(
            select(Category).where(Category.name == name)
        )
        return result.scalars().first()

    async def create(self, category: Category) -> Category:
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def update(self, id: int, category_data: Category) -> Optional[Category]:
        category = await self.get(id)
        if category:
            category.sqlmodel_update(category_data)
            await self.session.commit()
            await self.session.refresh(category)
            return category
        return None

    async def delete(self, id: int) -> bool:
        category = await self.get(id)
        if category:
            await self.session.delete(category)
            await self.session.commit()
            return True
        return False
