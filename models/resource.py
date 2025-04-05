from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import Relationship, SQLModel, Field

from models.category import Category
from models.user import User

class ResourceType(str, Enum):
    DOCUMENTO = "documento"
    RECURSO_RA = "recurso_ra"

class ResourceBase(SQLModel):
    description: Optional[str]
    type: ResourceType


class ResourceCreate(ResourceBase):
    name: str
    user_id: int
    url: str

class ResourceRead(ResourceBase):
    name: str
    url: str
    is_enabled: bool
    category_id: Optional[int]
    user_id: int

class Resource(ResourceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True)
    url: str = Field(default=None, unique=True)
    is_enabled: Optional[bool] = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional[Category] = Relationship(back_populates="resources")
    user_id: int = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="resources")