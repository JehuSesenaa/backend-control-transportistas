from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Sequence
from app.features.unidades.api.dependencies import get_unidad_service
from app.features.unidades.services.unidad_service import UnidadService
from app.features.unidades.schemas.unidad_schemas import UnidadCreate, UnidadUpdate, UnidadRead
from app.features.unidades.models.unidad import Unidad

router = APIRouter(prefix="/units", tags=["units"])


@router.post("", response_model=UnidadRead, status_code=201)
def create_unidad(unidad_create: UnidadCreate, service: UnidadService = Depends(get_unidad_service)) -> Unidad:
    return service.create_unidad(unidad_create)


@router.get("", response_model=Sequence[UnidadRead])
def get_unidades(
    offset: int = Query(default=0, ge=0, description="Número de registros a saltar (paginación)"),
    limit: int = Query(default=100, ge=1, le=100, description="Número máximo de registros a devolver"),
    service: UnidadService = Depends(get_unidad_service)
) -> Sequence[Unidad]:
    return service.get_all_unidades(offset, limit)

@router.get("/{unidad_id}", response_model=UnidadRead)
def get_unidad(unidad_id: int, service: UnidadService = Depends(get_unidad_service)) -> Unidad:
    unidad = service.get_unidad_by_id(unidad_id)
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")
    return unidad


@router.patch("/{unidad_id}", response_model=UnidadRead)
def update_unidad(
    unidad_id: int,
    unidad_update: UnidadUpdate,
    service: UnidadService = Depends(get_unidad_service)
) -> Unidad:
    unidad = service.update_unidad(unidad_id, unidad_update)
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")
    return unidad


@router.delete("/{unidad_id}", status_code=204)
def delete_unidad(unidad_id: int, service: UnidadService = Depends(get_unidad_service)) -> None:
    service.delete_unidad(unidad_id)
