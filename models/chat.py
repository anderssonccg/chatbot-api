from typing import Optional, Any
from datetime import datetime
from sqlmodel import Relationship, SQLModel, Field
from models.user import User

class ChatBase(SQLModel):
    titulo: str


class ChatCreateRequest(ChatBase):
    pass


class ChatCreate(ChatBase):
    user_id: int


class ChatUpdate(SQLModel):
    titulo: Optional[str] = None
    satisfaction_level: Optional[int] = Field(default=None, ge=1, le=5)


class ChatRead(ChatBase):
    id: int
    titulo: str
    fecha: datetime
    user_id: int
    satisfaction_level: Optional[int] = None
    messages: list[Any] = []

class Chat(ChatBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str = Field(default=None)
    fecha: datetime = Field(default_factory=datetime.utcnow)
    satisfaction_level: Optional[int] = Field(default=None, ge=1, le=5)
    user_id: int = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="chats")
    messages: list["Message"] = Relationship(back_populates="chat")