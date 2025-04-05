from typing import TYPE_CHECKING, Optional
from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from models.resource import Resource


class CategoryBase(SQLModel):
    name: str
    description: str


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    pass


class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    resources: list["Resource"] = Relationship(back_populates="category")
