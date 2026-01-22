from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from app.core.db.base import Base


class Rendimiento(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    route_id: int = Field(foreign_key="ruta.id", unique=True, index=True)
    distance_traveled_km: float = Field(default=0.0)
    fuel_consumed_liters: float = Field(default=0.0)
    actual_time_hours: float = Field(default=0.0)
    average_speed_kmh: float = Field(default=0.0)
    efficiency_score: float = Field(default=0.0)
    fuel_efficiency_km_per_liter: float = Field(default=0.0)
    time_efficiency: float = Field(default=0.0)
    notes: Optional[str] = Field(default=None, max_length=1000)
    recorded_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
