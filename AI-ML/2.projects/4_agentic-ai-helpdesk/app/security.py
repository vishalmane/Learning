import re
import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request


PII_PATTERNS = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
]

INJECTION_MARKERS = (
    "ignore previous instructions",
    "reveal system prompt",
    "developer message",
    "bypass policy",
)


def detect_pii(text: str) -> bool:
    return any(pattern.search(text) for pattern in PII_PATTERNS)


def looks_like_prompt_injection(text: str) -> bool:
    lower = text.lower()
    return any(marker in lower for marker in INJECTION_MARKERS)


class InMemoryRateLimiter:
    def __init__(self, limit_per_minute: int) -> None:
        self.limit = limit_per_minute
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    async def check(self, request: Request) -> None:
        client = request.client.host if request.client else "unknown"
        now = time.time()
        window = self._hits[client]
        while window and now - window[0] > 60:
            window.popleft()
        if len(window) >= self.limit:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        window.append(now)

