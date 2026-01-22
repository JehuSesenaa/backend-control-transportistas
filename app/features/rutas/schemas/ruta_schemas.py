from typing import Optional
from sqlmodel import SQLModel
from datetime import datetime
from app.features.rutas.models.ruta import RouteStatus


class RutaBase(SQLModel):
    origin: str
    destination: str
    distance_km: float
    estimated_time_hours: float
    unit_id: int


class RutaCreate(RutaBase):
    pass


class RutaUpdate(SQLModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    distance_km: Optional[float] = None
    estimated_time_hours: Optional[float] = None


class RutaRead(RutaBase):
    id: int
    status: RouteStatus
    assigned_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]


class RutaStatusUpdate(SQLModel):
    status: RouteStatus
