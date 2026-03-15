import json
import logging
from typing import Optional

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

EXPLANATION_PROMPT = """You are an expert exam tutor. A student answered a question incorrectly.

Question: {question}
Choices:
{choices}
Correct Answer: {correct_answer}
Student's Answer: {student_answer}

Respond ONLY with a JSON object (no markdown fences) in this exact format:
{{
  "explanation": "Clear explanation of the correct answer",
  "why_wrong": "Why the student's answer is incorrect",
  "topics_to_review": ["topic1", "topic2"]
}}"""


async def generate_explanation(
    question_text: str,
    choices: list[dict],
    correct_answer: str,
    student_answer: str,
) -> Optional[dict]:
    if not settings.LLM_API_KEY:
        logger.warning("LLM_API_KEY not configured; skipping AI explanation")
        return None

    choices_text = "\n".join(
        f"  {'[CORRECT] ' if c.get('is_correct') else ''}{c['choice_text']}"
        for c in choices
    )
    prompt = EXPLANATION_PROMPT.format(
        question=question_text,
        choices=choices_text,
        correct_answer=correct_answer,
        student_answer=student_answer,
    )

    headers = {
        "Authorization": f"Bearer {settings.LLM_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(settings.LLM_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            return json.loads(content)
    except Exception as exc:
        logger.error("LLM API error: %s", exc)
        return None
