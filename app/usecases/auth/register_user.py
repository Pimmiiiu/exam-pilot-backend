from app.core.security import hash_password
from app.domain.entities.user import UserEntity
from app.domain.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest
from fastapi import HTTPException, status


def register_user(request: RegisterRequest, repo: UserRepository) -> UserEntity:
    existing = repo.get_by_email(request.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    password_hash = hash_password(request.password)
    return repo.create(email=request.email, password_hash=password_hash)
