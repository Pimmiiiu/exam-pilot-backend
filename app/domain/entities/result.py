from dataclasses import dataclass
from typing import List, Optional


@dataclass
class AIExplanationEntity:
    id: str
    question_id: str
    wrong_choice_id: str
    explanation: str
    topics_to_review: List[str]
