from typing import Optional
from sqlmodel import SQLModel
from datetime import datetime


class RendimientoBase(SQLModel):
    route_id: int
    distance_traveled_km: float
    fuel_consumed_liters: float
    actual_time_hours: float


class RendimientoCreate(RendimientoBase):
    notes: Optional[str] = None


class RendimientoUpdate(SQLModel):
    distance_traveled_km: Optional[float] = None
    fuel_consumed_liters: Optional[float] = None
    actual_time_hours: Optional[float] = None
    notes: Optional[str] = None


class RendimientoRead(RendimientoBase):
    id: int
    average_speed_kmh: float
    efficiency_score: float
    fuel_efficiency_km_per_liter: float
    time_efficiency: float
    notes: Optional[str]
    recorded_at: datetime
    created_at: datetime
