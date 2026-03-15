from app.domain.repositories.exam_repository import ExamRepository
from app.domain.repositories.result_repository import ResultRepository
from app.schemas.result import ResultResponse, AnswerResultSchema
from fastapi import HTTPException, status


def calculate_result(
    attempt_id: str,
    exam_repo: ExamRepository,
    result_repo: ResultRepository,
) -> ResultResponse:
    attempt = result_repo.get_attempt(attempt_id)
    if not attempt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found")

    questions = exam_repo.get_questions(attempt.exam_id)
    question_map = {q.id: q for q in questions}

    user_answers = result_repo.get_user_answers(attempt_id)

    correct_answers = []
    incorrect_answers = []
    recommended_topics = set()

    for ua in user_answers:
        question = question_map.get(ua.question_id)
        if not question:
            continue
        choices = question.choices or []
        choice_map = {c.id: c for c in choices}
        correct_choice = next((c for c in choices if c.is_correct), None)
        selected_choice = choice_map.get(ua.selected_choice_id)

        answer_schema = AnswerResultSchema(
            question_id=ua.question_id,
            question_text=question.question_text,
            selected_choice_id=ua.selected_choice_id,
            selected_choice_text=selected_choice.choice_text if selected_choice else "",
            correct_choice_id=correct_choice.id if correct_choice else "",
            correct_choice_text=correct_choice.choice_text if correct_choice else "",
            is_correct=ua.is_correct,
        )
        if ua.is_correct:
            correct_answers.append(answer_schema)
        else:
            incorrect_answers.append(answer_schema)
            if question.topic:
                recommended_topics.add(question.topic)

    percentage = (
        round(attempt.score / attempt.total * 100, 2) if attempt.total > 0 else 0.0
    )

    return ResultResponse(
        attempt_id=attempt.id,
        exam_id=attempt.exam_id,
        score=attempt.score,
        total=attempt.total,
        percentage=percentage,
        time_spent=attempt.time_spent,
        correct_answers=correct_answers,
        incorrect_answers=incorrect_answers,
        recommended_topics=list(recommended_topics),
    )
