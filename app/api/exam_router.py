from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.exam_repository_impl import ExamRepositoryImpl
from app.infrastructure.repositories.result_repository_impl import ResultRepositoryImpl
from app.schemas.exam import ExamDetail, ExamListItem, SubmitExamRequest
from app.schemas.result import ResultResponse
from app.usecases.exam.get_exam_detail import get_exam_detail
from app.usecases.exam.get_exams import get_exams
from app.usecases.exam.submit_exam import submit_exam

router = APIRouter(prefix="/exams", tags=["exams"])


@router.get("", response_model=List[ExamListItem])
def list_exams(db: Annotated[Session, Depends(get_db)], _=Depends(get_current_user)):
    repo = ExamRepositoryImpl(db)
    return get_exams(repo)


@router.get("/{exam_id}", response_model=ExamDetail)
def get_exam(exam_id: str, db: Annotated[Session, Depends(get_db)], _=Depends(get_current_user)):
    repo = ExamRepositoryImpl(db)
    return get_exam_detail(exam_id, repo)


@router.post("/submit", response_model=ResultResponse)
def submit(
    request: SubmitExamRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user=Depends(get_current_user),
):
    exam_repo = ExamRepositoryImpl(db)
    result_repo = ResultRepositoryImpl(db)
    return submit_exam(request, current_user.id, exam_repo, result_repo)
