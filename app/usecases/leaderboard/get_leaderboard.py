from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.infrastructure.db.models import User, ExamAttempt
from app.schemas.leaderboard import LeaderboardEntry, LeaderboardResponse


def get_leaderboard(db: Session, limit: int = 50) -> LeaderboardResponse:
    rows = (
        db.query(
            User.id.label("user_id"),
            User.email.label("email"),
            func.sum(ExamAttempt.score).label("total_score"),
        )
        .join(ExamAttempt, ExamAttempt.user_id == User.id)
        .group_by(User.id, User.email)
        .order_by(desc("total_score"))
        .limit(limit)
        .all()
    )
    entries = [
        LeaderboardEntry(
            rank=i + 1,
            user_id=str(row.user_id),
            email=row.email,
            total_score=int(row.total_score or 0),
        )
        for i, row in enumerate(rows)
    ]
    return LeaderboardResponse(entries=entries)
