from datetime import datetime
from typing import Optional, Sequence
from sqlmodel import Session, select, or_
from app.features.rutas.models.ruta import Ruta, RouteStatus
from app.features.rutas.schemas.ruta_schemas import RutaCreate, RutaUpdate


class RutaRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, ruta_create: RutaCreate) -> Ruta:
        db_ruta = Ruta(**ruta_create.model_dump())
        self.session.add(db_ruta)
        self.session.commit()
        self.session.refresh(db_ruta)
        return db_ruta

    def get_by_id(self, ruta_id: int) -> Optional[Ruta]:
        statement = select(Ruta).where(Ruta.id == ruta_id)
        result = self.session.exec(statement).first()
        return result

    def get_by_unit_id(
        self, 
        unit_id: int, 
        status: Optional[RouteStatus] = None,
        offset: int = 0, 
        limit: int = 100
    ) -> Sequence[Ruta]:
        statement = select(Ruta).where(Ruta.unit_id == unit_id)
        if status:
            statement = statement.where(Ruta.status == status)
        statement = statement.offset(offset).limit(limit)
        result = self.session.exec(statement).all()
        return result

    def get_all(
        self, 
        status: Optional[RouteStatus] = None,
        unit_id: Optional[int] = None,
        offset: int = 0, 
        limit: int = 100
    ) -> Sequence[Ruta]:
        statement = select(Ruta)
        if status:
            statement = statement.where(Ruta.status == status)
        if unit_id:
            statement = statement.where(Ruta.unit_id == unit_id)
        statement = statement.offset(offset).limit(limit)
        result = self.session.exec(statement).all()
        return result

    def update(self, ruta: Ruta, ruta_update: RutaUpdate) -> Ruta:
        ruta_data = ruta_update.model_dump(exclude_unset=True)
        for key, value in ruta_data.items():
            setattr(ruta, key, value)
        self.session.add(ruta)
        self.session.commit()
        self.session.refresh(ruta)
        return ruta

    def update_status(self, ruta: Ruta, status: RouteStatus) -> Ruta:
        ruta.status = status
        if status == RouteStatus.EN_RUTA and not ruta.started_at:
            ruta.started_at = datetime.utcnow()
        if status == RouteStatus.COMPLETADA and not ruta.completed_at:
            ruta.completed_at = datetime.utcnow()
        self.session.add(ruta)
        self.session.commit()
        self.session.refresh(ruta)
        return ruta

    def delete(self, ruta: Ruta) -> bool:
        self.session.delete(ruta)
        self.session.commit()
        return True
