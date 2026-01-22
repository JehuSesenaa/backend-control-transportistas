from fastapi import APIRouter, Depends, HTTPException
from typing import Sequence
from sqlmodel import Session
from app.core.db.session import get_session
from app.features.users.api.dependencies import get_user_service
from app.features.users.services.user_service import UserService
from app.features.users.schemas.user_schemas import UserCreate, UserUpdate, UserRead
from app.features.users.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=201)
def create_user(user_create: UserCreate, service: UserService = Depends(get_user_service)) -> User:
    existing_user = service.get_user_by_email(user_create.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return service.create_user(user_create)


@router.get("/", response_model=Sequence[UserRead])
def get_users(
    offset: int = 0,
    limit: int = 100,
    service: UserService = Depends(get_user_service)
) -> Sequence[User]:
    return service.get_all_users(offset, limit)


@router.get("", response_model=Sequence[UserRead])
def get_users_no_trailing_slash(
    offset: int = 0,
    limit: int = 100,
    service: UserService = Depends(get_user_service)
) -> Sequence[User]:
    # Compatibility: handle /users (without trailing slash) without redirect
    return service.get_all_users(offset, limit)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, service: UserService = Depends(get_user_service)) -> User:
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    service: UserService = Depends(get_user_service)
) -> User:
    user = service.update_user(user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)) -> None:
    success = service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
