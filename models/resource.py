from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import Column, ForeignKey, Integer, Relationship, SQLModel, Field

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


class ResourceUpdate(SQLModel):
    category_id: Optional[int]


class ResourceUpdateStatus(SQLModel):
    is_enabled: bool

class ResourceRead(ResourceBase):
    id: int
    name: str
    url: str
    is_enabled: bool
    category_id: Optional[int]
    user_id: int
    model_config = {"from_attributes": True}


class Resource(ResourceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True)
    url: str = Field(default=None, unique=True)
    is_enabled: Optional[bool] = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    category_id: Optional[int] = Field(
        default=None,
        sa_column=Column(
            Integer, ForeignKey("category.id", ondelete="SET NULL"), nullable=True
        ),
    )
    category: Optional[Category] = Relationship(back_populates="resources")
    user_id: int = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="resources")
