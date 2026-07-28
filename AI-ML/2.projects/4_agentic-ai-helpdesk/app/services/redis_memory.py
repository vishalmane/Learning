import json
from collections import defaultdict, deque
from typing import Any

from app.config import get_settings


class RedisMemoryStore:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._client = None
        self._fallback: dict[str, deque[dict[str, Any]]] = defaultdict(lambda: deque(maxlen=20))
        try:
            import redis

            self._client = redis.Redis.from_url(self.settings.redis_url, decode_responses=True)
            self._client.ping()
        except Exception:
            self._client = None

    def load_memory(self, user_id: str) -> list[dict[str, Any]]:
        key = self._key(user_id)
        if self._client:
            return [json.loads(item) for item in self._client.lrange(key, 0, -1)]
        return list(self._fallback[user_id])

    def save_memory(self, user_id: str, item: dict[str, Any]) -> None:
        key = self._key(user_id)
        if self._client:
            self._client.rpush(key, json.dumps(item, default=str))
            self._client.expire(key, self.settings.redis_ttl_seconds)
            return
        self._fallback[user_id].append(item)

    def search_memory(self, user_id: str, text: str) -> list[dict[str, Any]]:
        needle = text.lower()
        return [item for item in self.load_memory(user_id) if needle in json.dumps(item).lower()]

    @staticmethod
    def _key(user_id: str) -> str:
        return f"helpdesk:memory:{user_id}"

