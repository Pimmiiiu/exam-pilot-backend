from typing import List, Optional
from pydantic import BaseModel


class AIExplanationSchema(BaseModel):
    explanation: str
    why_wrong: Optional[str] = None
    topics_to_review: List[str] = []


class AnswerResultSchema(BaseModel):
    question_id: str
    question_text: str
    selected_choice_id: str
    selected_choice_text: str
    correct_choice_id: str
    correct_choice_text: str
    is_correct: bool
    ai_explanation: Optional[AIExplanationSchema] = None


class ResultResponse(BaseModel):
    attempt_id: str
    exam_id: str
    score: int
    total: int
    percentage: float
    time_spent: Optional[int] = None
    correct_answers: List[AnswerResultSchema] = []
    incorrect_answers: List[AnswerResultSchema] = []
    recommended_topics: List[str] = []
