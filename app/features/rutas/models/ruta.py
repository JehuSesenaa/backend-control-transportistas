from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum
from app.core.db.base import Base


class RouteStatus(str, Enum):
    ASIGNADA = "ASIGNADA"
    EN_RUTA = "EN_RUTA"
    COMPLETADA = "COMPLETADA"
    CANCELADA = "CANCELADA"


class Ruta(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    origin: str = Field(max_length=255)
    destination: str = Field(max_length=255)
    distance_km: float = Field(default=0.0)
    estimated_time_hours: float = Field(default=0.0)
    status: RouteStatus = Field(default=RouteStatus.ASIGNADA)
    unit_id: int = Field(foreign_key="unidad.id", index=True)
    assigned_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
