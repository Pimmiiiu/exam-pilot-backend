from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.exam_repository_impl import ExamRepositoryImpl
from app.infrastructure.repositories.result_repository_impl import ResultRepositoryImpl
from app.schemas.result import ResultResponse
from app.usecases.result.calculate_result import calculate_result

router = APIRouter(prefix="/results", tags=["results"])


@router.get("/{attempt_id}", response_model=ResultResponse)
def get_result(
    attempt_id: str,
    db: Annotated[Session, Depends(get_db)],
    current_user=Depends(get_current_user),
):
    exam_repo = ExamRepositoryImpl(db)
    result_repo = ResultRepositoryImpl(db)
    attempt = result_repo.get_attempt(attempt_id)
    if attempt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found")
    if attempt.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return calculate_result(attempt_id, exam_repo, result_repo)
