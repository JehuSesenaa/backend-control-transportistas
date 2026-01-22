from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Sequence
from app.features.rendimiento.api.dependencies import get_rendimiento_service
from app.features.rendimiento.services.rendimiento_service import RendimientoService
from app.features.rendimiento.schemas.rendimiento_schemas import RendimientoCreate, RendimientoUpdate, RendimientoRead
from app.features.rendimiento.models.rendimiento import Rendimiento

router = APIRouter(prefix="/performance", tags=["performance"])


@router.post("/", response_model=RendimientoRead, status_code=201)
def create_rendimiento(
    rendimiento_create: RendimientoCreate,
    service: RendimientoService = Depends(get_rendimiento_service)
) -> Rendimiento:
    return service.create_rendimiento(rendimiento_create)


@router.get("/", response_model=Sequence[RendimientoRead])
def get_rendimientos(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    service: RendimientoService = Depends(get_rendimiento_service)
) -> Sequence[Rendimiento]:
    return service.get_all_rendimientos(offset, limit)


@router.get("/{rendimiento_id}", response_model=RendimientoRead)
def get_rendimiento(
    rendimiento_id: int,
    service: RendimientoService = Depends(get_rendimiento_service)
) -> Rendimiento:
    rendimiento = service.get_rendimiento_by_id(rendimiento_id)
    if not rendimiento:
        raise HTTPException(status_code=404, detail="Rendimiento not found")
    return rendimiento


@router.get("/route/{route_id}", response_model=RendimientoRead)
def get_rendimiento_by_route(
    route_id: int,
    service: RendimientoService = Depends(get_rendimiento_service)
) -> Rendimiento:
    rendimiento = service.get_rendimiento_by_route(route_id)
    if not rendimiento:
        raise HTTPException(status_code=404, detail="Rendimiento not found for this route")
    return rendimiento


@router.patch("/{rendimiento_id}", response_model=RendimientoRead)
def update_rendimiento(
    rendimiento_id: int,
    rendimiento_update: RendimientoUpdate,
    service: RendimientoService = Depends(get_rendimiento_service)
) -> Rendimiento:
    rendimiento = service.update_rendimiento(rendimiento_id, rendimiento_update)
    if not rendimiento:
        raise HTTPException(status_code=404, detail="Rendimiento not found")
    return rendimiento


@router.delete("/{rendimiento_id}", status_code=204)
def delete_rendimiento(
    rendimiento_id: int,
    service: RendimientoService = Depends(get_rendimiento_service)
) -> None:
    service.delete_rendimiento(rendimiento_id)
