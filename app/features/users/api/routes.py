from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Sequence
from sqlmodel import Session
from app.core.db.session import get_session
from app.features.users.api.dependencies import get_user_service
from app.features.users.services.user_service import UserService
from app.features.users.schemas.user_schemas import UserCreate, UserUpdate, UserRead
from app.features.users.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=201)
def create_user(user_create: UserCreate, service: UserService = Depends(get_user_service)) -> User:
    existing_user = service.get_user_by_email(user_create.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
    return service.create_user(user_create)


@router.get("", response_model=Sequence[UserRead])
def get_users(
    offset: int = Query(default=0, ge=0, description="Número de registros a saltar (paginación)"),
    limit: int = Query(default=100, ge=1, le=100, description="Número máximo de registros a devolver"),
    service: UserService = Depends(get_user_service)
) -> Sequence[User]:
    return service.get_all_users(offset, limit)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, service: UserService = Depends(get_user_service)) -> User:
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    service: UserService = Depends(get_user_service)
) -> User:
    user = service.update_user(user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)) -> None:
    success = service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
