from typing import Optional, Sequence
from passlib.context import CryptContext
from app.features.users.repositories.user_repository import UserRepository
from app.features.users.schemas.user_schemas import UserCreate, UserUpdate
from app.features.users.models.user import User


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def create_user(self, user_create: UserCreate) -> User:
        hashed_password = self.hash_password(user_create.password)
        return self.repository.create(user_create, hashed_password)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.repository.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.repository.get_by_email(email)

    def get_all_users(self, offset: int = 0, limit: int = 100) -> Sequence[User]:
        return self.repository.get_all(offset, limit)

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        user = self.repository.get_by_id(user_id)
        if not user:
            return None
        return self.repository.update(user, user_update)

    def delete_user(self, user_id: int) -> bool:
        user = self.repository.get_by_id(user_id)
        if not user:
            return False
        return self.repository.delete(user)
