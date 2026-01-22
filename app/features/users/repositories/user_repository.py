from typing import Optional, Sequence
from datetime import datetime
from sqlmodel import Session, select
from app.features.users.models.user import User
from app.features.users.schemas.user_schemas import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user_create: UserCreate, hashed_password: str) -> User:
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            full_name=user_create.full_name,
            phone=user_create.phone,
            hashed_password=hashed_password
        )
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def get_by_id(self, user_id: int) -> Optional[User]:
        statement = select(User).where(User.id == user_id)
        result = self.session.exec(statement).first()
        return result

    def get_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        result = self.session.exec(statement).first()
        return result

    def get_all(self, offset: int = 0, limit: int = 100) -> Sequence[User]:
        statement = select(User).offset(offset).limit(limit)
        result = self.session.exec(statement).all()
        return result

    def update(self, user: User, user_update: UserUpdate) -> User:
        user_data = user_update.model_dump(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user, key, value)
        user.updated_at = datetime.utcnow()
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User) -> bool:
        self.session.delete(user)
        self.session.commit()
        return True
