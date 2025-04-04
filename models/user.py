from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import datetime


class UserRole(str, Enum):
    ESTUDIANTE = "estudiante"
    DOCENTE = "docente"
    ADMIN = "admin"


class UserBase(SQLModel):
    fullname: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str
    role: Optional[UserRole] = Field(default="estudiante")
    is_active: Optional[bool] = Field(default=True)
    is_verified: Optional[bool] = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}
    )


class UserRead(UserBase):
    id: int
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

class UserPasswordReset(SQLModel):
    password: str
    confirm_password: str

class UserPasswordRequest(SQLModel):
    email: str