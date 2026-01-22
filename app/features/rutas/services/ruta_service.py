from typing import Optional, Sequence
from fastapi import HTTPException
from app.features.rutas.repositories.ruta_repository import RutaRepository
from app.features.rutas.schemas.ruta_schemas import RutaCreate, RutaUpdate, RutaStatusUpdate
from app.features.rutas.models.ruta import Ruta, RouteStatus
from app.features.unidades.repositories.unidad_repository import UnidadRepository


class RutaService:
    def __init__(self, repository: RutaRepository, unidad_repository: UnidadRepository):
        self.repository = repository
        self.unidad_repository = unidad_repository

    def create_ruta(self, ruta_create: RutaCreate) -> Ruta:
        unidad = self.unidad_repository.get_by_id(ruta_create.unit_id)
        if not unidad:
            raise HTTPException(status_code=404, detail="Unidad no encontrada")

        if not unidad.is_active:
            raise HTTPException(status_code=400, detail="La unidad no está activa")

        if ruta_create.distance_km <= 0:
            raise HTTPException(status_code=400, detail="La distancia debe ser mayor a 0")

        if ruta_create.estimated_time_hours <= 0:
            raise HTTPException(status_code=400, detail="El tiempo estimado debe ser mayor a 0")

        return self.repository.create(ruta_create)

    def get_ruta_by_id(self, ruta_id: int) -> Optional[Ruta]:
        return self.repository.get_by_id(ruta_id)

    def get_rutas_by_unit(
        self, 
        unit_id: int, 
        status: Optional[RouteStatus] = None,
        offset: int = 0, 
        limit: int = 100
    ) -> Sequence[Ruta]:
        unidad = self.unidad_repository.get_by_id(unit_id)
        if not unidad:
            raise HTTPException(status_code=404, detail="Unidad no encontrada")
        return self.repository.get_by_unit_id(unit_id, status, offset, limit)

    def get_all_rutas(
        self,
        status: Optional[RouteStatus] = None,
        unit_id: Optional[int] = None,
        offset: int = 0,
        limit: int = 100
    ) -> Sequence[Ruta]:
        if unit_id:
            unidad = self.unidad_repository.get_by_id(unit_id)
            if not unidad:
                raise HTTPException(status_code=404, detail="Unidad no encontrada")
        return self.repository.get_all(status, unit_id, offset, limit)

    def update_ruta(self, ruta_id: int, ruta_update: RutaUpdate) -> Optional[Ruta]:
        ruta = self.repository.get_by_id(ruta_id)
        if not ruta:
            raise HTTPException(status_code=404, detail="Ruta no encontrada")

        if ruta.status == RouteStatus.COMPLETADA:
            raise HTTPException(status_code=400, detail="No se puede actualizar una ruta completada")

        if ruta_update.distance_km is not None and ruta_update.distance_km <= 0:
            raise HTTPException(status_code=400, detail="La distancia debe ser mayor a 0")

        if ruta_update.estimated_time_hours is not None and ruta_update.estimated_time_hours <= 0:
            raise HTTPException(status_code=400, detail="El tiempo estimado debe ser mayor a 0")

        return self.repository.update(ruta, ruta_update)

    def update_ruta_status(self, ruta_id: int, status_update: RutaStatusUpdate) -> Optional[Ruta]:
        ruta = self.repository.get_by_id(ruta_id)
        if not ruta:
            raise HTTPException(status_code=404, detail="Ruta no encontrada")

        current_status = ruta.status
        new_status = status_update.status

        if current_status == RouteStatus.COMPLETADA:
            raise HTTPException(status_code=400, detail="No se puede cambiar el estado de una ruta completada")

        if current_status == RouteStatus.CANCELADA:
            raise HTTPException(status_code=400, detail="No se puede cambiar el estado de una ruta cancelada")

        valid_transitions = {
            RouteStatus.ASIGNADA: [RouteStatus.EN_RUTA, RouteStatus.CANCELADA],
            RouteStatus.EN_RUTA: [RouteStatus.COMPLETADA, RouteStatus.CANCELADA],
        }

        if new_status not in valid_transitions.get(current_status, []):
            raise HTTPException(
                status_code=400, 
                detail=f"Transición de estado inválida from {current_status} to {new_status}"
            )

        return self.repository.update_status(ruta, new_status)

    def delete_ruta(self, ruta_id: int) -> bool:
        ruta = self.repository.get_by_id(ruta_id)
        if not ruta:
            raise HTTPException(status_code=404, detail="Ruta no encontrada")

        if ruta.status == RouteStatus.EN_RUTA:
            raise HTTPException(status_code=400, detail="No se puede eliminar una ruta que está en progreso")

        return self.repository.delete(ruta)
