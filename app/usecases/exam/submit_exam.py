from app.domain.repositories.exam_repository import ExamRepository
from app.domain.repositories.result_repository import ResultRepository
from app.schemas.exam import SubmitExamRequest
from app.schemas.result import ResultResponse
from fastapi import HTTPException, status


def submit_exam(
    request: SubmitExamRequest,
    user_id: str,
    exam_repo: ExamRepository,
    result_repo: ResultRepository,
) -> ResultResponse:
    exam = exam_repo.get_by_id(request.exam_id)
    if not exam:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")

    questions = exam_repo.get_questions(request.exam_id)
    question_map = {q.id: q for q in questions}

    answers_to_save = []
    score = 0
    total = len(questions)

    submitted_ids = {a.question_id for a in request.answers}
    for q_id in question_map:
        if q_id not in submitted_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Answer missing for question {q_id}",
            )

    for answer in request.answers:
        question = question_map.get(answer.question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Question {answer.question_id} not found in exam",
            )
        choice_ids = {c.id for c in (question.choices or [])}
        if answer.selected_choice_id not in choice_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Choice {answer.selected_choice_id} is invalid for question {answer.question_id}",
            )
        is_correct = any(
            c.id == answer.selected_choice_id and c.is_correct
            for c in (question.choices or [])
        )
        if is_correct:
            score += 1
        answers_to_save.append(
            {
                "question_id": answer.question_id,
                "selected_choice_id": answer.selected_choice_id,
                "is_correct": is_correct,
            }
        )

    attempt = result_repo.create_attempt(
        user_id=user_id,
        exam_id=request.exam_id,
        score=score,
        total=total,
        time_spent=request.time_spent,
    )
    result_repo.save_user_answers(attempt.id, answers_to_save)

    percentage = round(score / total * 100, 2) if total > 0 else 0.0

    return ResultResponse(
        attempt_id=attempt.id,
        exam_id=attempt.exam_id,
        score=score,
        total=total,
        percentage=percentage,
        time_spent=request.time_spent,
    )
