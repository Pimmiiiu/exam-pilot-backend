from typing import Optional, List
from pydantic import BaseModel


class ChoiceSchema(BaseModel):
    id: str
    choice_text: str
    is_correct: bool


class QuestionSchema(BaseModel):
    id: str
    question_text: str
    topic: Optional[str] = None
    difficulty: Optional[str] = None
    choices: List[ChoiceSchema] = []


class ExamListItem(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    level: Optional[str] = None
    time_limit: Optional[int] = None


class ExamDetail(ExamListItem):
    questions: List[QuestionSchema] = []


class AnswerSubmit(BaseModel):
    question_id: str
    selected_choice_id: str


class SubmitExamRequest(BaseModel):
    exam_id: str
    answers: List[AnswerSubmit]
    time_spent: Optional[int] = None


class CreateExamRequest(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    level: Optional[str] = None
    time_limit: Optional[int] = None


class CreateChoiceRequest(BaseModel):
    choice_text: str
    is_correct: bool = False


class CreateQuestionRequest(BaseModel):
    question_text: str
    explanation: Optional[str] = None
    topic: Optional[str] = None
    difficulty: Optional[str] = None
    choices: List[CreateChoiceRequest] = []
