
from typing import Optional
from sqlmodel import Relationship, SQLModel, Field
from models.user import User


class FAQBase(SQLModel):
    question: str
    answer: str

class FAQCreate(FAQBase):
    pass

class FAQ(FAQBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question: str = Field(default=None)
    answer: str = Field(default=None)
    user_id: int = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="faqs")