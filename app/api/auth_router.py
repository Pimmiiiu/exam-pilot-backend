from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.usecases.auth.login_user import login_user
from app.usecases.auth.register_user import register_user
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(request: RegisterRequest, db: Annotated[Session, Depends(get_db)]):
    repo = UserRepositoryImpl(db)
    user = register_user(request, repo)
    return UserResponse(id=user.id, email=user.email, role=user.role)


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Annotated[Session, Depends(get_db)]):
    repo = UserRepositoryImpl(db)
    return login_user(request, repo)


@router.get("/me", response_model=UserResponse)
def me(current_user=Depends(get_current_user)):
    return UserResponse(id=current_user.id, email=current_user.email, role=current_user.role)
