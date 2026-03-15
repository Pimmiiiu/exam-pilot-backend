from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.infrastructure.db.session import get_db
from app.schemas.analytics import UserProgressResponse
from app.usecases.analytics.calculate_exam_stats import get_user_progress

router = APIRouter(prefix="/users", tags=["analytics"])


@router.get("/progress", response_model=UserProgressResponse)
def user_progress(
    db: Annotated[Session, Depends(get_db)],
    current_user=Depends(get_current_user),
):
    return get_user_progress(current_user.id, db)
