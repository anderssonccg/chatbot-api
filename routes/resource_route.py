
from typing import List
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from dependencies import check_role, get_current_user, get_resource_service
from models.resource import ResourceRead, ResourceType
from models.user import UserRead
from services.resource_service import ResourceService


router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("/", response_model=List[ResourceRead])
async def get_resources(user: UserRead = Depends(check_role("admin")), service: ResourceService = Depends(get_resource_service)):
    return await service.get_all_resources()

@router.get("/{resource_id}", response_model=ResourceRead)
async def get_resources(resource_id: int, user: UserRead = Depends(check_role("admin")), service: ResourceService = Depends(get_resource_service)):
    return await service.get_resource_by_id(resource_id)

@router.post("/")
async def upload_resource(
    description: str = Form(...),
    type: ResourceType = Form(...),
    user: UserRead = Depends(check_role("admin")),
    file: UploadFile = File(...),
    service: ResourceService = Depends(get_resource_service),
):
    
    resource_dict = {
        "name": "",
        "description": description,
        "type": type,
        "user_id": user.id,
        "url": "",
    }
    return await service.create_resource(file, resource_dict)