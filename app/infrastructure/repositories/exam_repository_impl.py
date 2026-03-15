from typing import Optional, List

from sqlalchemy.orm import Session, joinedload

from app.domain.entities.exam import ExamEntity
from app.domain.entities.question import QuestionEntity, ChoiceEntity
from app.domain.repositories.exam_repository import ExamRepository
from app.infrastructure.db.models import Exam, Question, Choice


def _exam_to_entity(exam: Exam) -> ExamEntity:
    return ExamEntity(
        id=str(exam.id),
        title=exam.title,
        description=exam.description,
        category=exam.category,
        level=exam.level,
        time_limit=exam.time_limit,
    )


def _question_to_entity(q: Question) -> QuestionEntity:
    choices = [
        ChoiceEntity(
            id=str(c.id),
            question_id=str(c.question_id),
            choice_text=c.choice_text,
            is_correct=c.is_correct,
        )
        for c in (q.choices or [])
    ]
    return QuestionEntity(
        id=str(q.id),
        exam_id=str(q.exam_id),
        question_text=q.question_text,
        explanation=q.explanation,
        topic=q.topic,
        difficulty=q.difficulty,
        choices=choices,
    )


class ExamRepositoryImpl(ExamRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[ExamEntity]:
        exams = self.db.query(Exam).all()
        return [_exam_to_entity(e) for e in exams]

    def get_by_id(self, exam_id: str) -> Optional[ExamEntity]:
        exam = self.db.query(Exam).filter(Exam.id == exam_id).first()
        return _exam_to_entity(exam) if exam else None

    def create_exam(self, title: str, description: str, category: str, level: str, time_limit: int) -> ExamEntity:
        exam = Exam(title=title, description=description, category=category, level=level, time_limit=time_limit)
        self.db.add(exam)
        self.db.commit()
        self.db.refresh(exam)
        return _exam_to_entity(exam)

    def get_questions(self, exam_id: str) -> List[QuestionEntity]:
        questions = (
            self.db.query(Question)
            .options(joinedload(Question.choices))
            .filter(Question.exam_id == exam_id)
            .all()
        )
        return [_question_to_entity(q) for q in questions]

    def get_question_by_id(self, question_id: str) -> Optional[QuestionEntity]:
        question = (
            self.db.query(Question)
            .options(joinedload(Question.choices))
            .filter(Question.id == question_id)
            .first()
        )
        return _question_to_entity(question) if question else None

    def add_question(self, exam_id: str, question_text: str, explanation: str, topic: str, difficulty: str, choices: list) -> QuestionEntity:
        question = Question(
            exam_id=exam_id,
            question_text=question_text,
            explanation=explanation,
            topic=topic,
            difficulty=difficulty,
        )
        self.db.add(question)
        self.db.flush()
        for c in choices:
            choice = Choice(
                question_id=str(question.id),
                choice_text=c["choice_text"],
                is_correct=c.get("is_correct", False),
            )
            self.db.add(choice)
        self.db.commit()
        self.db.refresh(question)
        return _question_to_entity(question)
