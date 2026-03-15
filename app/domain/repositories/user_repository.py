from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.entities.user import UserEntity


class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[UserEntity]:
        ...

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        ...

    @abstractmethod
    def create(self, email: str, password_hash: str, role: str = "student") -> UserEntity:
        ...

    @abstractmethod
    def list_all(self) -> List[UserEntity]:
        ...
