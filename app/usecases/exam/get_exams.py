from typing import List
from app.domain.repositories.exam_repository import ExamRepository
from app.schemas.exam import ExamListItem


def get_exams(repo: ExamRepository) -> List[ExamListItem]:
    exams = repo.get_all()
    return [
        ExamListItem(
            id=e.id,
            title=e.title,
            description=e.description,
            category=e.category,
            level=e.level,
            time_limit=e.time_limit,
        )
        for e in exams
    ]
