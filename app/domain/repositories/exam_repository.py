from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.entities.exam import ExamEntity
from app.domain.entities.question import QuestionEntity


class ExamRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[ExamEntity]:
        ...

    @abstractmethod
    def get_by_id(self, exam_id: str) -> Optional[ExamEntity]:
        ...

    @abstractmethod
    def create_exam(self, title: str, description: str, category: str, level: str, time_limit: int) -> ExamEntity:
        ...

    @abstractmethod
    def get_questions(self, exam_id: str) -> List[QuestionEntity]:
        ...

    @abstractmethod
    def add_question(self, exam_id: str, question_text: str, explanation: str, topic: str, difficulty: str, choices: list) -> QuestionEntity:
        ...
