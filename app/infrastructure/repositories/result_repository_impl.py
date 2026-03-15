from typing import Optional, List

from sqlalchemy.orm import Session

from app.domain.entities.attempt import ExamAttemptEntity, UserAnswerEntity
from app.domain.entities.result import AIExplanationEntity
from app.domain.repositories.result_repository import ResultRepository
from app.infrastructure.db.models import ExamAttempt, UserAnswer, AIExplanation


def _attempt_to_entity(a: ExamAttempt) -> ExamAttemptEntity:
    return ExamAttemptEntity(
        id=str(a.id),
        user_id=str(a.user_id),
        exam_id=str(a.exam_id),
        score=a.score,
        total=a.total,
        time_spent=a.time_spent,
        created_at=a.created_at,
    )


def _answer_to_entity(ua: UserAnswer) -> UserAnswerEntity:
    return UserAnswerEntity(
        id=str(ua.id),
        attempt_id=str(ua.attempt_id),
        question_id=str(ua.question_id),
        selected_choice_id=str(ua.selected_choice_id),
        is_correct=ua.is_correct,
    )


def _explanation_to_entity(e: AIExplanation) -> AIExplanationEntity:
    topics = e.topics_to_review if isinstance(e.topics_to_review, list) else []
    return AIExplanationEntity(
        id=str(e.id),
        question_id=str(e.question_id),
        wrong_choice_id=str(e.wrong_choice_id),
        explanation=e.explanation,
        topics_to_review=topics,
    )


class ResultRepositoryImpl(ResultRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_attempt(self, user_id: str, exam_id: str, score: int, total: int, time_spent: int) -> ExamAttemptEntity:
        attempt = ExamAttempt(
            user_id=user_id, exam_id=exam_id, score=score, total=total, time_spent=time_spent
        )
        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)
        return _attempt_to_entity(attempt)

    def get_attempt(self, attempt_id: str) -> Optional[ExamAttemptEntity]:
        attempt = self.db.query(ExamAttempt).filter(ExamAttempt.id == attempt_id).first()
        return _attempt_to_entity(attempt) if attempt else None

    def save_user_answers(self, attempt_id: str, answers: list) -> List[UserAnswerEntity]:
        saved = []
        for a in answers:
            ua = UserAnswer(
                attempt_id=attempt_id,
                question_id=a["question_id"],
                selected_choice_id=a["selected_choice_id"],
                is_correct=a["is_correct"],
            )
            self.db.add(ua)
            saved.append(ua)
        self.db.commit()
        for ua in saved:
            self.db.refresh(ua)
        return [_answer_to_entity(ua) for ua in saved]

    def get_user_answers(self, attempt_id: str) -> List[UserAnswerEntity]:
        answers = self.db.query(UserAnswer).filter(UserAnswer.attempt_id == attempt_id).all()
        return [_answer_to_entity(ua) for ua in answers]

    def get_ai_explanation(self, question_id: str, wrong_choice_id: str) -> Optional[AIExplanationEntity]:
        exp = (
            self.db.query(AIExplanation)
            .filter(
                AIExplanation.question_id == question_id,
                AIExplanation.wrong_choice_id == wrong_choice_id,
            )
            .first()
        )
        return _explanation_to_entity(exp) if exp else None

    def save_ai_explanation(self, question_id: str, wrong_choice_id: str, explanation: str, topics_to_review: list) -> AIExplanationEntity:
        exp = AIExplanation(
            question_id=question_id,
            wrong_choice_id=wrong_choice_id,
            explanation=explanation,
            topics_to_review=topics_to_review,
        )
        self.db.add(exp)
        self.db.commit()
        self.db.refresh(exp)
        return _explanation_to_entity(exp)

    def get_user_attempts(self, user_id: str) -> List[ExamAttemptEntity]:
        attempts = (
            self.db.query(ExamAttempt)
            .filter(ExamAttempt.user_id == user_id)
            .order_by(ExamAttempt.created_at.desc())
            .all()
        )
        return [_attempt_to_entity(a) for a in attempts]
