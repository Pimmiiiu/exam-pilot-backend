from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class ExamAttemptEntity:
    id: str
    user_id: str
    exam_id: str
    score: int
    total: int
    time_spent: Optional[int]
    created_at: datetime


@dataclass
class UserAnswerEntity:
    id: str
    attempt_id: str
    question_id: str
    selected_choice_id: str
    is_correct: bool
