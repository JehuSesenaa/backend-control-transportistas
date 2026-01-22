from typing import Optional, Sequence
from fastapi import HTTPException
from app.features.unidades.repositories.unidad_repository import UnidadRepository
from app.features.unidades.schemas.unidad_schemas import UnidadCreate, UnidadUpdate
from app.features.unidades.models.unidad import Unidad
from app.features.users.repositories.user_repository import UserRepository


class UnidadService:
    def __init__(self, repository: UnidadRepository, user_repository: UserRepository):
        self.repository = repository
        self.user_repository = user_repository

    def create_unidad(self, unidad_create: UnidadCreate) -> Unidad:
        user = self.user_repository.get_by_id(unidad_create.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        existing_unidad = self.repository.get_by_license_plate(unidad_create.license_plate)
        if existing_unidad:
            raise HTTPException(status_code=400, detail="License plate already registered")

        if unidad_create.year < 1900 or unidad_create.year > 2026:
            raise HTTPException(status_code=400, detail="Invalid year")

        if unidad_create.capacity <= 0:
            raise HTTPException(status_code=400, detail="Capacity must be greater than 0")

        return self.repository.create(unidad_create)

    def get_unidad_by_id(self, unidad_id: int) -> Optional[Unidad]:
        return self.repository.get_by_id(unidad_id)

    def get_unidades_by_user(self, user_id: int, offset: int = 0, limit: int = 100) -> Sequence[Unidad]:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return self.repository.get_by_user_id(user_id, offset, limit)

    def get_all_unidades(self, offset: int = 0, limit: int = 100) -> Sequence[Unidad]:
        return self.repository.get_all(offset, limit)

    def update_unidad(self, unidad_id: int, unidad_update: UnidadUpdate) -> Optional[Unidad]:
        unidad = self.repository.get_by_id(unidad_id)
        if not unidad:
            raise HTTPException(status_code=404, detail="Unidad not found")

        if unidad_update.license_plate:
            existing = self.repository.check_license_plate_exists(unidad_update.license_plate, unidad_id)
            if existing:
                raise HTTPException(status_code=400, detail="License plate already registered")

        if unidad_update.year is not None:
            if unidad_update.year < 1900 or unidad_update.year > 2026:
                raise HTTPException(status_code=400, detail="Invalid year")

        if unidad_update.capacity is not None and unidad_update.capacity <= 0:
            raise HTTPException(status_code=400, detail="Capacity must be greater than 0")

        return self.repository.update(unidad, unidad_update)

    def delete_unidad(self, unidad_id: int) -> bool:
        unidad = self.repository.get_by_id(unidad_id)
        if not unidad:
            raise HTTPException(status_code=404, detail="Unidad not found")
        return self.repository.delete(unidad)
