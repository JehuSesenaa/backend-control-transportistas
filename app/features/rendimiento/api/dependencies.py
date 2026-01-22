from fastapi import Depends
from sqlmodel import Session
from app.core.db.session import get_session
from app.features.rendimiento.repositories.rendimiento_repository import RendimientoRepository
from app.features.rendimiento.services.rendimiento_service import RendimientoService
from app.features.rutas.repositories.ruta_repository import RutaRepository
from app.features.rutas.api.dependencies import get_ruta_repository


def get_rendimiento_repository(session: Session = Depends(get_session)) -> RendimientoRepository:
    return RendimientoRepository(session)


def get_rendimiento_service(
    repository: RendimientoRepository = Depends(get_rendimiento_repository),
    ruta_repository: RutaRepository = Depends(get_ruta_repository)
) -> RendimientoService:
    return RendimientoService(repository, ruta_repository)
