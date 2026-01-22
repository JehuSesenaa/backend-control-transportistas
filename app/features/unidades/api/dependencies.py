from fastapi import Depends
from sqlmodel import Session
from app.core.db.session import get_session
from app.core.db.session import get_session as get_session_unidad
from app.features.unidades.repositories.unidad_repository import UnidadRepository
from app.features.unidades.services.unidad_service import UnidadService
from app.features.users.repositories.user_repository import UserRepository
from app.features.users.api.dependencies import get_user_repository


def get_unidad_repository(session: Session = Depends(get_session_unidad)) -> UnidadRepository:
    return UnidadRepository(session)


def get_unidad_service(
    repository: UnidadRepository = Depends(get_unidad_repository),
    user_repository: UserRepository = Depends(get_user_repository)
) -> UnidadService:
    return UnidadService(repository, user_repository)
