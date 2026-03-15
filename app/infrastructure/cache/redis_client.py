import json
import logging
import threading
from typing import Optional

import redis

from app.core.config import settings

logger = logging.getLogger(__name__)

_redis_client: Optional[redis.Redis] = None
_redis_lock = threading.Lock()


def get_redis() -> Optional[redis.Redis]:
    global _redis_client
    if _redis_client is not None:
        return _redis_client
    with _redis_lock:
        if _redis_client is None:
            try:
                client = redis.from_url(settings.REDIS_URL, decode_responses=True)
                client.ping()
                _redis_client = client
            except Exception as exc:
                logger.warning("Redis unavailable: %s", exc)
    return _redis_client


def cache_get(key: str) -> Optional[dict]:
    client = get_redis()
    if client is None:
        return None
    try:
        value = client.get(key)
        return json.loads(value) if value else None
    except Exception as exc:
        logger.warning("Redis GET error: %s", exc)
        return None


def cache_set(key: str, value: dict, ttl: int = 3600) -> None:
    client = get_redis()
    if client is None:
        return
    try:
        client.setex(key, ttl, json.dumps(value))
    except Exception as exc:
        logger.warning("Redis SET error: %s", exc)
