from typing import Optional, List

from sqlalchemy.orm import Session

from app.domain.entities.user import UserEntity
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.db.models import User


def _to_entity(user: User) -> UserEntity:
    return UserEntity(
        id=str(user.id),
        email=user.email,
        password_hash=user.password_hash,
        role=user.role.value if hasattr(user.role, "value") else user.role,
        created_at=user.created_at,
        is_active=user.is_active,
    )


class UserRepositoryImpl(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str) -> Optional[UserEntity]:
        user = self.db.query(User).filter(User.id == user_id).first()
        return _to_entity(user) if user else None

    def get_by_email(self, email: str) -> Optional[UserEntity]:
        user = self.db.query(User).filter(User.email == email).first()
        return _to_entity(user) if user else None

    def create(self, email: str, password_hash: str, role: str = "student") -> UserEntity:
        user = User(email=email, password_hash=password_hash, role=role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return _to_entity(user)

    def list_all(self) -> List[UserEntity]:
        users = self.db.query(User).all()
        return [_to_entity(u) for u in users]
