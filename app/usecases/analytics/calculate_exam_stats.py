from sqlalchemy.orm import Session
from sqlalchemy import func

from app.infrastructure.db.models import ExamAttempt, UserAnswer, Question
from app.schemas.analytics import UserProgressResponse, WeakTopic, ExamStatsResponse

WEAK_TOPIC_ACCURACY_THRESHOLD = 70.0


def get_user_progress(user_id: str, db: Session) -> UserProgressResponse:
    attempts = db.query(ExamAttempt).filter(ExamAttempt.user_id == user_id).all()
    total_exams = len(attempts)
    avg_score = (
        sum(a.score / a.total * 100 for a in attempts if a.total > 0) / total_exams
        if total_exams > 0
        else 0.0
    )

    attempt_ids = [a.id for a in attempts]
    wrong_by_topic = (
        db.query(Question.topic, func.count(UserAnswer.id).label("wrong_count"))
        .join(UserAnswer, UserAnswer.question_id == Question.id)
        .filter(
            UserAnswer.attempt_id.in_(attempt_ids),
            UserAnswer.is_correct.is_(False),
            Question.topic.is_not(None),
        )
        .group_by(Question.topic)
        .all()
    )
    total_by_topic = (
        db.query(Question.topic, func.count(UserAnswer.id).label("total_count"))
        .join(UserAnswer, UserAnswer.question_id == Question.id)
        .filter(
            UserAnswer.attempt_id.in_(attempt_ids),
            Question.topic.is_not(None),
        )
        .group_by(Question.topic)
        .all()
    )
    total_map = {row.topic: row.total_count for row in total_by_topic}
    wrong_map = {row.topic: row.wrong_count for row in wrong_by_topic}

    weak_topics = []
    for topic, wrong in wrong_map.items():
        total = total_map.get(topic, 0)
        accuracy = round((1 - wrong / total) * 100, 2) if total > 0 else 0.0
        if accuracy < WEAK_TOPIC_ACCURACY_THRESHOLD:
            weak_topics.append(WeakTopic(topic=topic, accuracy=accuracy))
    weak_topics.sort(key=lambda t: t.accuracy)

    return UserProgressResponse(
        user_id=user_id,
        total_exams_taken=total_exams,
        average_score=round(avg_score, 2),
        weak_topics=weak_topics,
    )


def get_exam_stats(exam_id: str, db: Session) -> ExamStatsResponse:
    attempts = db.query(ExamAttempt).filter(ExamAttempt.exam_id == exam_id).all()
    total_attempts = len(attempts)
    avg_score = (
        sum(a.score / a.total * 100 for a in attempts if a.total > 0) / total_attempts
        if total_attempts > 0
        else 0.0
    )
    time_values = [a.time_spent for a in attempts if a.time_spent is not None]
    avg_time = sum(time_values) / len(time_values) if time_values else None
    return ExamStatsResponse(
        exam_id=exam_id,
        total_attempts=total_attempts,
        average_score=round(avg_score, 2),
        average_time_spent=round(avg_time, 2) if avg_time else None,
    )
