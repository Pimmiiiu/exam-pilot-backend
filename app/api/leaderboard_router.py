from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.infrastructure.db.session import get_db
from app.schemas.leaderboard import LeaderboardResponse
from app.usecases.leaderboard.get_leaderboard import get_leaderboard

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("", response_model=LeaderboardResponse)
def leaderboard(
    db: Annotated[Session, Depends(get_db)],
    limit: int = Query(default=50, ge=1, le=100),
    _=Depends(get_current_user),
):
    return get_leaderboard(db, limit=limit)
