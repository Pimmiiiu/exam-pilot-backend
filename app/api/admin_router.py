import csv
import io
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.exam_repository_impl import ExamRepositoryImpl
from app.schemas.exam import (
    CreateExamRequest,
    CreateQuestionRequest,
    ExamListItem,
    QuestionSchema,
    ChoiceSchema,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/exams", response_model=ExamListItem, status_code=201)
def create_exam(
    request: CreateExamRequest,
    db: Annotated[Session, Depends(get_db)],
    _=Depends(require_admin),
):
    repo = ExamRepositoryImpl(db)
    exam = repo.create_exam(
        title=request.title,
        description=request.description or "",
        category=request.category or "",
        level=request.level or "",
        time_limit=request.time_limit or 0,
    )
    return ExamListItem(
        id=exam.id,
        title=exam.title,
        description=exam.description,
        category=exam.category,
        level=exam.level,
        time_limit=exam.time_limit,
    )


@router.post("/questions", response_model=QuestionSchema, status_code=201)
def create_question(
    exam_id: str,
    request: CreateQuestionRequest,
    db: Annotated[Session, Depends(get_db)],
    _=Depends(require_admin),
):
    repo = ExamRepositoryImpl(db)
    exam = repo.get_by_id(exam_id)
    if not exam:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
    choices = [{"choice_text": c.choice_text, "is_correct": c.is_correct} for c in request.choices]
    question = repo.add_question(
        exam_id=exam_id,
        question_text=request.question_text,
        explanation=request.explanation or "",
        topic=request.topic or "",
        difficulty=request.difficulty or "",
        choices=choices,
    )
    return QuestionSchema(
        id=question.id,
        question_text=question.question_text,
        topic=question.topic,
        difficulty=question.difficulty,
        choices=[ChoiceSchema(id=c.id, choice_text=c.choice_text, is_correct=c.is_correct) for c in (question.choices or [])],
    )


@router.post("/questions/import", status_code=201)
async def import_questions(
    exam_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only CSV files are supported")

    repo = ExamRepositoryImpl(db)
    exam = repo.get_by_id(exam_id)
    if not exam:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")

    content = await file.read()
    text = content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    expected_fields = {"question", "choiceA", "choiceB", "choiceC", "choiceD", "correct"}
    if not expected_fields.issubset(set(reader.fieldnames or [])):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"CSV must contain columns: {', '.join(sorted(expected_fields))}",
        )

    imported = 0
    for row in reader:
        correct_label = row["correct"].strip().upper()
        choice_map = {
            "A": row["choiceA"].strip(),
            "B": row["choiceB"].strip(),
            "C": row["choiceC"].strip(),
            "D": row["choiceD"].strip(),
        }
        choices = [
            {"choice_text": text, "is_correct": label == correct_label}
            for label, text in choice_map.items()
        ]
        repo.add_question(
            exam_id=exam_id,
            question_text=row["question"].strip(),
            explanation="",
            topic="",
            difficulty="",
            choices=choices,
        )
        imported += 1

    return {"imported": imported, "exam_id": exam_id}
