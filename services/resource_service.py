
from typing import Optional

from fastapi import HTTPException, UploadFile, status
from models.resource import Resource, ResourceCreate, ResourceRead
from repositories.resource_repository import ResourceRepository
from utils.gcs import upload_file

class ResourceService:
    
    def __init__(self, resource_repository: ResourceRepository):
        self.resource_repository = resource_repository

    
    async def get_all_resources(self) -> list[ResourceRead]:
        resources = await self.resource_repository.get_all()
        return [ResourceRead.model_validate(resource) for resource in resources]
    
    async def get_resource_by_id(self, resource_id: int) -> Optional[ResourceRead]:
        resource = await self.resource_repository.get(resource_id)
        if not resource:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recurso inexistente.")
        return ResourceRead.model_validate(resource)

    async def create_resource(self, file: UploadFile, resource_dict: dict) -> ResourceRead:
        file_dict = upload_file(file)
        resource_dict["url"] = file_dict["url"]
        resource_dict["filename"] = file_dict["filename"]
        resource = Resource.model_validate(resource_dict)
        resource = await self.resource_repository.create(resource)
        return ResourceRead.model_validate(resource)