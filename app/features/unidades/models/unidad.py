from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from app.core.db.base import Base


class Unidad(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    license_plate: str = Field(unique=True, index=True, max_length=20)
    brand: str = Field(max_length=100)
    model: str = Field(max_length=100)
    year: int = Field(index=True)
    capacity: float = Field(default=0.0)
    user_id: int = Field(foreign_key="user.id", unique=True, index=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
