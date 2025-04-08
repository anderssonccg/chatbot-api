from typing import List, Optional
from fastapi import HTTPException, status
from models.category import (
    Category,
    CategoryCreate,
    CategoryRead,
    CategoryReadWithResources,
    CategoryUpdate,
)
from repositories.category_repository import CategoryRepository


class CategoryService:

    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    async def get_all_categories(self) -> List[CategoryRead]:
        categories = await self.category_repository.get_all()
        return [CategoryRead.model_validate(category) for category in categories]

    async def get_category_by_id(self, category_id) -> Optional[CategoryRead]:
        category = await self.category_repository.get(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Categoria inexistente."
            )
        return CategoryRead.model_validate(category)

    async def get_category_with_resources(
        self, category_id
    ) -> Optional[CategoryReadWithResources]:
        category = await self.category_repository.get_with_resources(category_id)
        return CategoryReadWithResources.model_validate(category)

    async def validate_name(self, name: str) -> Optional[CategoryRead]:
        category = await self.category_repository.get_by_name(name)
        if category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de la categoria ya esta en uso.",
            )

    async def create_category(self, category_data: CategoryCreate) -> CategoryRead:
        await self.validate_name(category_data.name)
        category = Category.model_validate(category_data)
        return await self.category_repository.create(category)
    
    async def update_category(self, category_id: int, category_data: CategoryUpdate) -> CategoryRead:
        category = await self.category_repository.get(category_id)
        if category_data.name and category_data.name != category.name:
            await self.validate_name(category_data.name)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria inexistente.")
        category_data = category_data.dict(exclude_unset=True)
        return await self.category_repository.update(category_id, category_data)

    async def delete_category(self, category_id: int) -> bool:
        deleted_category = await self.category_repository.delete(category_id)
        if not deleted_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Categoria inexistente."
            )
        return True
