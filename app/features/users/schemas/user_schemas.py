from typing import Optional
from sqlmodel import SQLModel
from datetime import datetime


class UserBase(SQLModel):
    email: str
    username: str
    full_name: str
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    email: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class UserRead(UserBase):
    id: int
    phone: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
