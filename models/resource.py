from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import Relationship, SQLModel, Field

from models.category import Category
from models.user import User

class ResourceType(str, Enum):
    DOCUMENTO = "documento"
    RECURSO_RA = "recurso"

class ResourceBase(SQLModel):
    name: str
    description: str
    type: ResourceType


class ResourceCreate(ResourceBase):
    category_id: Optional[int]
    user_id: int


class ResourceRead(ResourceBase):
    pass


class Resource(ResourceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    is_enabled: Optional[bool] = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional[Category] = Relationship(back_populates="resources")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="resources")