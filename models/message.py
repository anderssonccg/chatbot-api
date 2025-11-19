from typing import Optional
from datetime import datetime
from sqlmodel import Relationship, SQLModel, Field
from enum import Enum
from models.chat import Chat

class MessageRole(str, Enum):
    user = "user"
    chatbot = "chatbot"

class MessageBase(SQLModel):
    role: MessageRole
    texto: str

class MessageCreateRequest(MessageBase):
    pass

class MessageCreate(MessageBase):
    chat_id: int
    response_time: Optional[float] = None

class MessageUpdate(SQLModel):
    role: Optional[MessageRole] = None
    texto: Optional[str] = None

class MessageRead(MessageBase):
    id: int
    chat_id: int
    fecha: datetime

class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    chat_id: int = Field(default=None, foreign_key="chat.id")
    role: MessageRole
    texto: str = Field(default=None)
    fecha: datetime = Field(default_factory=datetime.utcnow)
    response_time: Optional[float] = Field(default=None)
    chat: Chat = Relationship(back_populates="messages")