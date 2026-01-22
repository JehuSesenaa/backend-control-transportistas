from typing import Optional
from sqlmodel import SQLModel
from datetime import datetime


class UnidadBase(SQLModel):
    license_plate: str
    brand: str
    model: str
    year: int
    capacity: float
    user_id: int


class UnidadCreate(UnidadBase):
    pass


class UnidadUpdate(SQLModel):
    license_plate: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    capacity: Optional[float] = None
    is_active: Optional[bool] = None


class UnidadRead(UnidadBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
