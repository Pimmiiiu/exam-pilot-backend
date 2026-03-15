import logging
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

_DEFAULT_SECRET_KEY = "change-me-in-production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "ExamPilot Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    SECRET_KEY: str = _DEFAULT_SECRET_KEY
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/exampilot"
    REDIS_URL: str = "redis://localhost:6379/0"

    # CORS — restrict to your frontend origin(s) in production
    CORS_ORIGINS: list[str] = ["*"]

    LLM_API_KEY: str = ""
    LLM_API_URL: str = "https://api.openai.com/v1/chat/completions"
    LLM_MODEL: str = "gpt-4o-mini"

    def validate_production_secrets(self) -> None:
        if not self.DEBUG and self.SECRET_KEY == _DEFAULT_SECRET_KEY:
            logger.warning(
                "SECRET_KEY is set to the insecure default value. "
                "Set a strong SECRET_KEY in production (e.g. `openssl rand -hex 32`)."
            )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
