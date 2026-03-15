from app.core.jwt import create_access_token, create_refresh_token
from app.core.security import verify_password
from app.domain.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse
from fastapi import HTTPException, status


def login_user(request: LoginRequest, repo: UserRepository) -> TokenResponse:
    user = repo.get_by_email(request.email)
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    access_token = create_access_token(subject=str(user.id), extra_claims={"role": user.role})
    refresh_token = create_refresh_token(subject=str(user.id))
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
