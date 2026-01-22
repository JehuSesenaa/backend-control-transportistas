from typing import Optional, Sequence
from datetime import datetime
from sqlmodel import Session, select
from app.features.unidades.models.unidad import Unidad
from app.features.unidades.schemas.unidad_schemas import UnidadCreate, UnidadUpdate


class UnidadRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, unidad_create: UnidadCreate) -> Unidad:
        db_unidad = Unidad(**unidad_create.model_dump())
        self.session.add(db_unidad)
        self.session.commit()
        self.session.refresh(db_unidad)
        return db_unidad

    def get_by_id(self, unidad_id: int) -> Optional[Unidad]:
        statement = select(Unidad).where(Unidad.id == unidad_id)
        result = self.session.exec(statement).first()
        return result

    def get_by_license_plate(self, license_plate: str) -> Optional[Unidad]:
        statement = select(Unidad).where(Unidad.license_plate == license_plate)
        result = self.session.exec(statement).first()
        return result

    def get_by_user_id(self, user_id: int) -> Optional[Unidad]:
        statement = select(Unidad).where(Unidad.user_id == user_id)
        result = self.session.exec(statement).first()
        return result

    def get_all(self, offset: int = 0, limit: int = 100) -> Sequence[Unidad]:
        statement = select(Unidad).offset(offset).limit(limit)
        result = self.session.exec(statement).all()
        return result

    def update(self, unidad: Unidad, unidad_update: UnidadUpdate) -> Unidad:
        unidad_data = unidad_update.model_dump(exclude_unset=True)
        for key, value in unidad_data.items():
            setattr(unidad, key, value)
        unidad.updated_at = datetime.utcnow()
        self.session.add(unidad)
        self.session.commit()
        self.session.refresh(unidad)
        return unidad

    def delete(self, unidad: Unidad) -> bool:
        self.session.delete(unidad)
        self.session.commit()
        return True

    def check_license_plate_exists(self, license_plate: str, exclude_id: Optional[int] = None) -> bool:
        statement = select(Unidad).where(Unidad.license_plate == license_plate)
        if exclude_id:
            statement = statement.where(Unidad.id != exclude_id)
        result = self.session.exec(statement).first()
        return result is not None
