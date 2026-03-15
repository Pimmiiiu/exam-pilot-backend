import logging
from typing import Optional

from app.domain.repositories.exam_repository import ExamRepository
from app.domain.repositories.result_repository import ResultRepository
from app.infrastructure.cache.redis_client import cache_get, cache_set
from app.infrastructure.ai.llm_service import generate_explanation
from app.schemas.result import AIExplanationSchema

logger = logging.getLogger(__name__)

CACHE_TTL = 86400  # 24 hours


async def get_ai_explanation_for_answer(
    question_id: str,
    wrong_choice_id: str,
    exam_repo: ExamRepository,
    result_repo: ResultRepository,
) -> Optional[AIExplanationSchema]:
    cache_key = f"ai_explanation:{question_id}:{wrong_choice_id}"
    cached = cache_get(cache_key)
    if cached:
        return AIExplanationSchema(**cached)

    db_explanation = result_repo.get_ai_explanation(question_id, wrong_choice_id)
    if db_explanation:
        schema = AIExplanationSchema(
            explanation=db_explanation.explanation,
            topics_to_review=db_explanation.topics_to_review,
        )
        cache_set(cache_key, schema.model_dump(), ttl=CACHE_TTL)
        return schema

    question = exam_repo.get_question_by_id(question_id)
    if not question:
        return None

    choices = question.choices or []
    wrong_choice = next((c for c in choices if c.id == wrong_choice_id), None)
    if not wrong_choice:
        return None
    correct_choice = next((c for c in choices if c.is_correct), None)

    llm_result = await generate_explanation(
        question_text=question.question_text,
        choices=[{"choice_text": c.choice_text, "is_correct": c.is_correct} for c in choices],
        correct_answer=correct_choice.choice_text if correct_choice else "",
        student_answer=wrong_choice.choice_text,
    )
    if llm_result is None:
        return None

    topics = llm_result.get("topics_to_review", [])
    explanation_text = llm_result.get("explanation", "")
    why_wrong = llm_result.get("why_wrong", "")

    result_repo.save_ai_explanation(
        question_id=question_id,
        wrong_choice_id=wrong_choice_id,
        explanation=explanation_text,
        topics_to_review=topics,
    )
    schema = AIExplanationSchema(
        explanation=explanation_text,
        why_wrong=why_wrong,
        topics_to_review=topics,
    )
    cache_set(cache_key, schema.model_dump(), ttl=CACHE_TTL)
    return schema
