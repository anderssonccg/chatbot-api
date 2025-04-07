from typing import TYPE_CHECKING, Optional
from sqlmodel import Relationship, SQLModel, Field
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Enum as PgEnum

if TYPE_CHECKING:
    from models.resource import Resource


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
    role: Optional[UserRole] = Field(
        default=UserRole.ESTUDIANTE,
        sa_column=Column(PgEnum(UserRole, name="userrole", create_type=False))
    )
    photo: Optional[str] = Field(default=None)
    is_active: Optional[bool] = Field(default=True)
    is_verified: Optional[bool] = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}
    )
    resources: list["Resource"] = Relationship(back_populates="user")

class UserRead(UserBase):
    id: int
    role: str
    photo: Optional[str]
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

class UserUpdate(SQLModel):
    fullname: str

class UserUpdateRole(SQLModel):
    role: UserRole

class UserUpdateStatus(SQLModel):
    is_active: bool

class UserPasswordReset(SQLModel):
    password: str
    confirm_password: str

class UserPasswordRequest(SQLModel):
    email: str
