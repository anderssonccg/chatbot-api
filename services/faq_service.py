from typing import List, Optional
from fastapi import HTTPException, status
from models.faq import FAQ, FAQCreate, FAQRead, FAQUpdate
from repositories.faq_repository import FAQRepository


class FAQService:

    def __init__(self, faq_repository: FAQRepository):
        self.faq_repository = faq_repository

    async def get_all_faqs(self) -> List[FAQRead]:
        faqs = await self.faq_repository.get_all()
        return [FAQRead.model_validate(faq) for faq in faqs]

    async def get_by_id(self, id: int) -> Optional[FAQRead]:
        faq = await self.faq_repository.get(id)
        if not faq:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pregunta inexistente."
            )
        return FAQRead.model_validate(faq)

    async def create(self, faq: FAQCreate) -> FAQRead:
        faq = FAQ.model_validate(faq.dict())
        faq_created = await self.faq_repository.create(faq)
        return FAQRead.model_validate(faq_created)

    async def update(self, faq_id: int, faq_data: FAQUpdate) -> FAQRead:
        await self.get_by_id(faq_id)
        faq_data = faq_data.dict(exclude_unset=True)
        faq_updated = await self.faq_repository.update(faq_id, faq_data)
        return FAQRead.model_validate(faq_updated)

    async def delete(self, faq_id: int) -> bool:
        await self.get_by_id(faq_id)
        return await self.faq_repository.delete(faq_id)
