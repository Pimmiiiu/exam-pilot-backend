from dataclasses import dataclass
from typing import Optional


@dataclass
class ExamEntity:
    id: str
    title: str
    description: Optional[str]
    category: Optional[str]
    level: Optional[str]
    time_limit: Optional[int]
