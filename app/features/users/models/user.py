from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from app.core.db.base import Base


class User(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True)
    full_name: str
    phone: Optional[str] = Field(default=None, max_length=20)
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
