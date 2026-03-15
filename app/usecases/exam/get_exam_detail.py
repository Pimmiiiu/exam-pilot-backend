from typing import Optional
from app.domain.repositories.exam_repository import ExamRepository
from app.schemas.exam import ExamDetail, QuestionSchema, ChoiceSchema
from fastapi import HTTPException, status


def get_exam_detail(exam_id: str, repo: ExamRepository) -> ExamDetail:
    exam = repo.get_by_id(exam_id)
    if not exam:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
    questions = repo.get_questions(exam_id)
    question_schemas = [
        QuestionSchema(
            id=q.id,
            question_text=q.question_text,
            topic=q.topic,
            difficulty=q.difficulty,
            choices=[
                ChoiceSchema(id=c.id, choice_text=c.choice_text, is_correct=c.is_correct)
                for c in (q.choices or [])
            ],
        )
        for q in questions
    ]
    return ExamDetail(
        id=exam.id,
        title=exam.title,
        description=exam.description,
        category=exam.category,
        level=exam.level,
        time_limit=exam.time_limit,
        questions=question_schemas,
    )
