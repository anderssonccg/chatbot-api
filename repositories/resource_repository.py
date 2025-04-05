from typing import List, Optional
from sqlmodel import select
from config.db import SessionDep
from models.resource import Resource, ResourceUpdate
from repositories.repository_interface import IRepository


class ResourceRepository(IRepository[Resource]):

    def __init__(self, session: SessionDep):
        self.session = session

    async def get_all(self) -> List[Resource]:
        result = await self.session.execute(select(Resource))
        return result.scalars().all()

    async def get(self, id: int) -> Optional[Resource]:
        result = await self.session.execute(select(Resource).where(Resource.id == id))
        return result.scalars().first()

    async def create(self, resource: Resource) -> Resource:
        self.session.add(resource)
        await self.session.commit()
        await self.session.refresh(resource)
        return resource

    async def update(
        self, id: int, resource_data: ResourceUpdate
    ) -> Optional[Resource]:
        resource = await self.get(id)
        if resource:
            resource.sqlmodel_update(resource_data)
            await self.session.commit()
            await self.session.refresh(resource)
            return resource
        return None

    async def delete(self, id: int) -> bool:
        resource = await self.get(id)
        if resource:
            await self.session.delete(resource)
            await self.session.commit()
            return True
        return False
