from dataclasses import dataclass
from typing import Optional, List


@dataclass
class ChoiceEntity:
    id: str
    question_id: str
    choice_text: str
    is_correct: bool


@dataclass
class QuestionEntity:
    id: str
    exam_id: str
    question_text: str
    explanation: Optional[str]
    topic: Optional[str]
    difficulty: Optional[str]
    choices: List[ChoiceEntity] = None
