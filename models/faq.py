from typing import Optional
from sqlmodel import Relationship, SQLModel, Field
from models.user import User


class FAQBase(SQLModel):
    question: str
    answer: str


class FAQCreateRequest(FAQBase):
    pass


class FAQCreate(FAQBase):
    user_id: int


class FAQUpdate(SQLModel):
    question: Optional[str] = None
    answer: Optional[str] = None


class FAQRead(FAQBase):
    id: int
    question: str
    answer: str
    user_id: int


class FAQ(FAQBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question: str = Field(default=None)
    answer: str = Field(default=None)
    user_id: int = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="faqs")
