from fastapi import Depends
from sqlmodel import Session
from app.core.db.session import get_session
from app.features.rutas.repositories.ruta_repository import RutaRepository
from app.features.rutas.services.ruta_service import RutaService
from app.features.unidades.repositories.unidad_repository import UnidadRepository
from app.features.unidades.api.dependencies import get_unidad_repository


def get_ruta_repository(session: Session = Depends(get_session)) -> RutaRepository:
    return RutaRepository(session)


def get_ruta_service(
    repository: RutaRepository = Depends(get_ruta_repository),
    unidad_repository: UnidadRepository = Depends(get_unidad_repository)
) -> RutaService:
    return RutaService(repository, unidad_repository)
