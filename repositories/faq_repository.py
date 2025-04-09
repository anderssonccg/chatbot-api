from typing import List, Optional
from sqlmodel import select
from config.db import SessionDep
from models.faq import FAQ
from repositories.repository_interface import IRepository


class FAQRepository(IRepository[FAQ]):

    def __init__(self, session: SessionDep):
        self.session = session

    async def get_all(self) -> List[FAQ]:
        result = await self.session.execute(select(FAQ))
        return result.scalars().all()

    async def get(self, id: int) -> Optional[FAQ]:
        result = await self.session.execute(select(FAQ).where(FAQ.id == id))
        return result.scalars().first()

    async def create(self, faq: FAQ) -> FAQ:
        self.session.add(faq)
        await self.session.commit()
        await self.session.refresh(faq)
        return faq

    async def update(self, id: int, faq_data: FAQ) -> Optional[FAQ]:
        faq = await self.get(id)
        if faq:
            faq.sqlmodel_update(faq_data)
            await self.session.commit()
            await self.session.refresh(faq)
            return faq
        return None

    async def delete(self, id: int) -> bool:
        faq = await self.get(id)
        if faq:
            await self.session.delete(faq)
            await self.session.commit()
            return True
        return False
