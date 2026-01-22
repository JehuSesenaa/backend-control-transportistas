from typing import Optional, Sequence
from sqlmodel import Session, select
from app.features.rendimiento.models.rendimiento import Rendimiento
from app.features.rendimiento.schemas.rendimiento_schemas import RendimientoCreate, RendimientoUpdate


class RendimientoRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, rendimiento_create: RendimientoCreate) -> Rendimiento:
        db_rendimiento = Rendimiento(**rendimiento_create.model_dump())
        self.session.add(db_rendimiento)
        self.session.commit()
        self.session.refresh(db_rendimiento)
        return db_rendimiento

    def get_by_id(self, rendimiento_id: int) -> Optional[Rendimiento]:
        statement = select(Rendimiento).where(Rendimiento.id == rendimiento_id)
        result = self.session.exec(statement).first()
        return result

    def get_by_route_id(self, route_id: int) -> Optional[Rendimiento]:
        statement = select(Rendimiento).where(Rendimiento.route_id == route_id)
        result = self.session.exec(statement).first()
        return result

    def get_all(self, offset: int = 0, limit: int = 100) -> Sequence[Rendimiento]:
        statement = select(Rendimiento).offset(offset).limit(limit)
        result = self.session.exec(statement).all()
        return result

    def update(self, rendimiento: Rendimiento, rendimiento_update: RendimientoUpdate) -> Rendimiento:
        rendimiento_data = rendimiento_update.model_dump(exclude_unset=True)
        for key, value in rendimiento_data.items():
            setattr(rendimiento, key, value)
        self.session.add(rendimiento)
        self.session.commit()
        self.session.refresh(rendimiento)
        return rendimiento

    def delete(self, rendimiento: Rendimiento) -> bool:
        self.session.delete(rendimiento)
        self.session.commit()
        return True
