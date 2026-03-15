import uuid
import enum
from datetime import datetime, timezone

from sqlalchemy import (
    Column, String, Boolean, Integer, DateTime, ForeignKey,
    Text, Enum as SAEnum, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship


def generate_uuid():
    return str(uuid.uuid4())


class Base(DeclarativeBase):
    pass


class UserRole(str, enum.Enum):
    student = "student"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(SAEnum(UserRole), default=UserRole.student, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    attempts = relationship("ExamAttempt", back_populates="user")


class Exam(Base):
    __tablename__ = "exams"

    id = Column(UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    level = Column(String(50), nullable=True)
    time_limit = Column(Integer, nullable=True)

    questions = relationship("Question", back_populates="exam", cascade="all, delete-orphan")
    attempts = relationship("ExamAttempt", back_populates="exam")


class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    exam_id = Column(UUID(as_uuid=False), ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    question_text = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    topic = Column(String(100), nullable=True)
    difficulty = Column(String(50), nullable=True)

    exam = relationship("Exam", back_populates="questions")
    choices = relationship("Choice", back_populates="question", cascade="all, delete-orphan")
    user_answers = relationship("UserAnswer", back_populates="question")
    ai_explanations = relationship("AIExplanation", back_populates="question")


class Choice(Base):
    __tablename__ = "choices"

    id = Column(UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    question_id = Column(UUID(as_uuid=False), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    choice_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False, nullable=False)

    question = relationship("Question", back_populates="choices")


class ExamAttempt(Base):
    __tablename__ = "exam_attempts"

    id = Column(UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    exam_id = Column(UUID(as_uuid=False), ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, default=0, nullable=False)
    total = Column(Integer, default=0, nullable=False)
    time_spent = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="attempts")
    exam = relationship("Exam", back_populates="attempts")
    user_answers = relationship("UserAnswer", back_populates="attempt", cascade="all, delete-orphan")


class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    attempt_id = Column(UUID(as_uuid=False), ForeignKey("exam_attempts.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(UUID(as_uuid=False), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    selected_choice_id = Column(UUID(as_uuid=False), ForeignKey("choices.id", ondelete="CASCADE"), nullable=False)
    is_correct = Column(Boolean, default=False, nullable=False)

    attempt = relationship("ExamAttempt", back_populates="user_answers")
    question = relationship("Question", back_populates="user_answers")
    selected_choice = relationship("Choice")


class AIExplanation(Base):
    __tablename__ = "ai_explanations"

    id = Column(UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    question_id = Column(UUID(as_uuid=False), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    wrong_choice_id = Column(UUID(as_uuid=False), ForeignKey("choices.id", ondelete="CASCADE"), nullable=False)
    explanation = Column(Text, nullable=False)
    topics_to_review = Column(JSON, default=list, nullable=False)

    question = relationship("Question", back_populates="ai_explanations")


class Leaderboard(Base):
    __tablename__ = "leaderboard"

    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    total_score = Column(Integer, default=0, nullable=False)
    rank = Column(Integer, nullable=True)

    user = relationship("User")
