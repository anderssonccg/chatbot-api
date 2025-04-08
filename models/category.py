from typing import TYPE_CHECKING, Optional
from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from models.resource import Resource, ResourceRead


class CategoryBase(SQLModel):
    name: str
    description: str


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int

class CategoryUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryReadWithResources(CategoryRead):
    resources: list["ResourceRead"] = []

    model_config = {"from_attributes": True}


class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None, unique=True)
    description: str = Field(default=None)
    resources: list["Resource"] = Relationship(back_populates="category")


from models.resource import ResourceRead

CategoryReadWithResources.model_rebuild()
