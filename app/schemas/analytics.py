from typing import List, Optional
from pydantic import BaseModel


class WeakTopic(BaseModel):
    topic: str
    accuracy: float


class UserProgressResponse(BaseModel):
    user_id: str
    total_exams_taken: int
    average_score: float
    weak_topics: List[WeakTopic] = []


class ExamStatsResponse(BaseModel):
    exam_id: str
    total_attempts: int
    average_score: float
    average_time_spent: Optional[float] = None
