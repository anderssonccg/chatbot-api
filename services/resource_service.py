import os
from typing import Optional

from fastapi import HTTPException, UploadFile, status
from models.resource import Resource, ResourceCreate, ResourceRead
from repositories.resource_repository import ResourceRepository
from utils import gcs


class ResourceService:

    def __init__(self, resource_repository: ResourceRepository):
        self.resource_repository = resource_repository

    async def get_all_resources(self) -> list[ResourceRead]:
        resources = await self.resource_repository.get_all()
        return [ResourceRead.model_validate(resource) for resource in resources]

    async def get_resource_by_id(self, resource_id: int) -> Optional[ResourceRead]:
        resource = await self.resource_repository.get(resource_id)
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Recurso inexistente."
            )
        return ResourceRead.model_validate(resource)

    async def create_resource(
        self, file: UploadFile, resource_dict: dict
    ) -> ResourceRead:
        
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Solo se permiten PDF.")

        ext = os.path.splitext(file.filename)[1].lower()
        if ext != ".pdf":
            raise HTTPException(status_code=400, detail="El archivo debe ser .pdf.")

        file_dict = gcs.upload_file(file)
        resource_dict["url"] = file_dict["url"]
        resource_dict["name"] = file_dict["filename"]
        resource = Resource.model_validate(resource_dict)
        resource = await self.resource_repository.create(resource)
        return ResourceRead.model_validate(resource)

    async def delete_resource(self, resource_id) -> bool:
        resource = await self.get_resource_by_id(resource_id)
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Recurso inexistente."
            )
        gcs.delete_file(resource.name)
        return await self.resource_repository.delete(resource.id)

    async def update_resource(self, resource_id, resource) -> ResourceRead:
        resource_update = await self.resource_repository.update(resource_id, resource)
        if not resource_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Recurso inexistente."
            )
        return ResourceRead.model_validate(resource_update)
