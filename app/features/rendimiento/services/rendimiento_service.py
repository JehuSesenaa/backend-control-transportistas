from typing import Optional, Sequence, Any
from fastapi import HTTPException
from app.features.rendimiento.repositories.rendimiento_repository import RendimientoRepository
from app.features.rendimiento.schemas.rendimiento_schemas import RendimientoCreate, RendimientoUpdate
from app.features.rendimiento.models.rendimiento import Rendimiento
from app.features.rutas.repositories.ruta_repository import RutaRepository
from app.features.rutas.models.ruta import RouteStatus


class RendimientoService:
    def __init__(
        self, 
        repository: RendimientoRepository,
        ruta_repository: RutaRepository
    ):
        self.repository = repository
        self.ruta_repository = ruta_repository

    def _calculate_metrics(
        self,
        distance_traveled_km: float,
        fuel_consumed_liters: float,
        actual_time_hours: float,
        ruta: Any
    ) -> dict:
        average_speed_kmh = distance_traveled_km / actual_time_hours if actual_time_hours > 0 else 0.0
        
        fuel_efficiency_km_per_liter = (
            distance_traveled_km / fuel_consumed_liters 
            if fuel_consumed_liters > 0 else 0.0
        )

        if ruta.estimated_time_hours > 0:
            time_efficiency = (ruta.estimated_time_hours / actual_time_hours) * 100
        else:
            time_efficiency = 100.0

        time_efficiency = max(0, min(100, time_efficiency))

        efficiency_score = (time_efficiency + min(100, fuel_efficiency_km_per_liter * 10)) / 2

        return {
            "average_speed_kmh": round(average_speed_kmh, 2),
            "fuel_efficiency_km_per_liter": round(fuel_efficiency_km_per_liter, 2),
            "time_efficiency": round(time_efficiency, 2),
            "efficiency_score": round(efficiency_score, 2)
        }

    def create_rendimiento(self, rendimiento_create: RendimientoCreate) -> Rendimiento:
        ruta = self.ruta_repository.get_by_id(rendimiento_create.route_id)
        if not ruta:
            raise HTTPException(status_code=404, detail="Ruta not found")

        if ruta.status != RouteStatus.COMPLETADA:
            raise HTTPException(
                status_code=400, 
                detail=f"Performance can only be recorded for completed routes. Current status: {ruta.status}"
            )

        existing_rendimiento = self.repository.get_by_route_id(rendimiento_create.route_id)
        if existing_rendimiento:
            raise HTTPException(
                status_code=400, 
                detail="Performance record already exists for this route"
            )

        if rendimiento_create.distance_traveled_km <= 0:
            raise HTTPException(status_code=400, detail="Distance traveled must be greater than 0")

        if rendimiento_create.fuel_consumed_liters <= 0:
            raise HTTPException(status_code=400, detail="Fuel consumed must be greater than 0")

        if rendimiento_create.actual_time_hours <= 0:
            raise HTTPException(status_code=400, detail="Actual time must be greater than 0")

        metrics = self._calculate_metrics(
            rendimiento_create.distance_traveled_km,
            rendimiento_create.fuel_consumed_liters,
            rendimiento_create.actual_time_hours,
            ruta
        )

        db_rendimiento = Rendimiento(
            route_id=rendimiento_create.route_id,
            distance_traveled_km=rendimiento_create.distance_traveled_km,
            fuel_consumed_liters=rendimiento_create.fuel_consumed_liters,
            actual_time_hours=rendimiento_create.actual_time_hours,
            notes=rendimiento_create.notes,
            **metrics
        )

        self.repository.session.add(db_rendimiento)
        self.repository.session.commit()
        self.repository.session.refresh(db_rendimiento)
        return db_rendimiento

    def get_rendimiento_by_id(self, rendimiento_id: int) -> Optional[Rendimiento]:
        return self.repository.get_by_id(rendimiento_id)

    def get_rendimiento_by_route(self, route_id: int) -> Optional[Rendimiento]:
        ruta = self.ruta_repository.get_by_id(route_id)
        if not ruta:
            raise HTTPException(status_code=404, detail="Ruta not found")
        return self.repository.get_by_route_id(route_id)

    def get_all_rendimientos(self, offset: int = 0, limit: int = 100) -> Sequence[Rendimiento]:
        return self.repository.get_all(offset, limit)

    def update_rendimiento(
        self, 
        rendimiento_id: int, 
        rendimiento_update: RendimientoUpdate
    ) -> Optional[Rendimiento]:
        rendimiento = self.repository.get_by_id(rendimiento_id)
        if not rendimiento:
            raise HTTPException(status_code=404, detail="Rendimiento not found")

        if rendimiento_update.distance_traveled_km is not None:
            if rendimiento_update.distance_traveled_km <= 0:
                raise HTTPException(status_code=400, detail="Distance traveled must be greater than 0")

        if rendimiento_update.fuel_consumed_liters is not None:
            if rendimiento_update.fuel_consumed_liters <= 0:
                raise HTTPException(status_code=400, detail="Fuel consumed must be greater than 0")

        if rendimiento_update.actual_time_hours is not None:
            if rendimiento_update.actual_time_hours <= 0:
                raise HTTPException(status_code=400, detail="Actual time must be greater than 0")

        update_data = rendimiento_update.model_dump(exclude_unset=True)

        needs_recalc = False
        for key in ["distance_traveled_km", "fuel_consumed_liters", "actual_time_hours"]:
            if key in update_data:
                needs_recalc = True
                break

        if needs_recalc:
            ruta = self.ruta_repository.get_by_id(rendimiento.route_id)
            distance = update_data.get("distance_traveled_km", rendimiento.distance_traveled_km)
            fuel = update_data.get("fuel_consumed_liters", rendimiento.fuel_consumed_liters)
            time_hours = update_data.get("actual_time_hours", rendimiento.actual_time_hours)

            metrics = self._calculate_metrics(distance, fuel, time_hours, ruta)
            update_data.update(metrics)

        for key, value in update_data.items():
            setattr(rendimiento, key, value)

        self.repository.session.add(rendimiento)
        self.repository.session.commit()
        self.repository.session.refresh(rendimiento)
        return rendimiento

    def delete_rendimiento(self, rendimiento_id: int) -> bool:
        rendimiento = self.repository.get_by_id(rendimiento_id)
        if not rendimiento:
            raise HTTPException(status_code=404, detail="Rendimiento not found")
        return self.repository.delete(rendimiento)
