from typing import List
from fastapi import APIRouter, Depends
from dependencies import check_role, get_category_service
from models.category import CategoryCreate, CategoryRead, CategoryReadWithResources, CategoryUpdate
from models.user import UserRead
from services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryRead])
async def get_all_categories(
    user: UserRead = Depends(check_role("admin")),
    service: CategoryService = Depends(get_category_service),
):
    return await service.get_all_categories()


@router.get("/{category_id}", response_model=CategoryRead)
async def get_category(
    category_id: int,
    user: UserRead = Depends(check_role("admin")),
    service: CategoryService = Depends(get_category_service),
):
    return await service.get_category_by_id(category_id)


@router.get("/{category_id}/with-resources", response_model=CategoryReadWithResources)
async def get_category_with_resources(
    category_id: int,
    user: UserRead = Depends(check_role("admin")),
    service: CategoryService = Depends(get_category_service),
):
    return await service.get_category_with_resources(category_id)


@router.post("/", response_model=CategoryRead)
async def create_category(
    category: CategoryCreate,
    user: UserRead = Depends(check_role("admin")),
    service: CategoryService = Depends(get_category_service),
):
    return await service.create_category(category)


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    user: UserRead = Depends(check_role("admin")),
    service: CategoryService = Depends(get_category_service),
):
    await service.delete_category(category_id)
    return {"message": "La categoria se ha eliminado exitosamente."}


@router.put("/{category_id}/update")
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    user: UserRead = Depends(check_role("admin")),
    service: CategoryService = Depends(get_category_service)
):
    return await service.update_category(category_id, category_data)
