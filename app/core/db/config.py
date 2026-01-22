from sqlmodel import create_engine, SQLModel
from app.core.config.settings import settings
from app.core.db.base import Base


def init_db():
    engine = create_engine(settings.DATABASE_URL, echo=True)
    SQLModel.metadata.create_all(engine)
