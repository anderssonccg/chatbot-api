from typing import List
from fastapi import APIRouter, Depends

from dependencies import check_role, get_faq_service
from models.faq import FAQCreate, FAQCreateRequest, FAQRead, FAQUpdate
from models.user import UserRead
from services.faq_service import FAQService


router = APIRouter(prefix="/faqs", tags=["FAQs"])


@router.get("/", response_model=List[FAQRead])
async def get_all_faqs(
    user: UserRead = Depends(check_role("admin")),
    service: FAQService = Depends(get_faq_service),
):
    return await service.get_all_faqs()


@router.get("/{faq_id}", response_model=FAQRead)
async def get_faq(
    faq_id: int,
    user: UserRead = Depends(check_role("admin")),
    service: FAQService = Depends(get_faq_service),
):
    return await service.get_by_id(faq_id)


@router.post("/", response_model=FAQRead)
async def create_faq(
    faq: FAQCreateRequest,
    user: UserRead = Depends(check_role("admin")),
    service: FAQService = Depends(get_faq_service),
):
    faq_dict = faq.dict()
    faq_dict["user_id"] = user.id
    return await service.create(FAQCreate.model_validate(faq_dict))


@router.put("/{faq_id}", response_model=FAQRead)
async def update_faq(
    faq_id: int,
    faq_data: FAQUpdate,
    user: UserRead = Depends(check_role("admin")),
    service: FAQService = Depends(get_faq_service),
):
    return await service.update(faq_id, faq_data)


@router.delete("/{faq_id}")
async def delete_faq(
    faq_id: int,
    user: UserRead = Depends(check_role("admin")),
    service: FAQService = Depends(get_faq_service),
):
    return await service.delete(faq_id)
