from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Sequence, Optional
from app.features.rutas.api.dependencies import get_ruta_service
from app.features.rutas.services.ruta_service import RutaService
from app.features.rutas.schemas.ruta_schemas import RutaCreate, RutaUpdate, RutaStatusUpdate, RutaRead
from app.features.rutas.models.ruta import Ruta, RouteStatus

router = APIRouter(prefix="/routes", tags=["routes"])


@router.post("/", response_model=RutaRead, status_code=201)
def create_ruta(ruta_create: RutaCreate, service: RutaService = Depends(get_ruta_service)) -> Ruta:
    return service.create_ruta(ruta_create)


@router.get("/", response_model=Sequence[RutaRead])
def get_rutas(
    status: Optional[RouteStatus] = Query(default=None),
    unit_id: Optional[int] = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    service: RutaService = Depends(get_ruta_service)
) -> Sequence[Ruta]:
    return service.get_all_rutas(status, unit_id, offset, limit)


@router.get("/{ruta_id}", response_model=RutaRead)
def get_ruta(ruta_id: int, service: RutaService = Depends(get_ruta_service)) -> Ruta:
    ruta = service.get_ruta_by_id(ruta_id)
    if not ruta:
        raise HTTPException(status_code=404, detail="Ruta not found")
    return ruta


@router.patch("/{ruta_id}", response_model=RutaRead)
def update_ruta(
    ruta_id: int,
    ruta_update: RutaUpdate,
    service: RutaService = Depends(get_ruta_service)
) -> Ruta:
    ruta = service.update_ruta(ruta_id, ruta_update)
    if not ruta:
        raise HTTPException(status_code=404, detail="Ruta not found")
    return ruta


@router.patch("/{ruta_id}/status", response_model=RutaRead)
def update_ruta_status(
    ruta_id: int,
    status_update: RutaStatusUpdate,
    service: RutaService = Depends(get_ruta_service)
) -> Ruta:
    ruta = service.update_ruta_status(ruta_id, status_update)
    if not ruta:
        raise HTTPException(status_code=404, detail="Ruta not found")
    return ruta


@router.delete("/{ruta_id}", status_code=204)
def delete_ruta(ruta_id: int, service: RutaService = Depends(get_ruta_service)) -> None:
    service.delete_ruta(ruta_id)
