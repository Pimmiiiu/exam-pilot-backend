from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.entities.attempt import ExamAttemptEntity, UserAnswerEntity
from app.domain.entities.result import AIExplanationEntity


class ResultRepository(ABC):
    @abstractmethod
    def create_attempt(self, user_id: str, exam_id: str, score: int, total: int, time_spent: int) -> ExamAttemptEntity:
        ...

    @abstractmethod
    def get_attempt(self, attempt_id: str) -> Optional[ExamAttemptEntity]:
        ...

    @abstractmethod
    def save_user_answers(self, attempt_id: str, answers: list) -> List[UserAnswerEntity]:
        ...

    @abstractmethod
    def get_user_answers(self, attempt_id: str) -> List[UserAnswerEntity]:
        ...

    @abstractmethod
    def get_ai_explanation(self, question_id: str, wrong_choice_id: str) -> Optional[AIExplanationEntity]:
        ...

    @abstractmethod
    def save_ai_explanation(self, question_id: str, wrong_choice_id: str, explanation: str, topics_to_review: list) -> AIExplanationEntity:
        ...

    @abstractmethod
    def get_user_attempts(self, user_id: str) -> List[ExamAttemptEntity]:
        ...
