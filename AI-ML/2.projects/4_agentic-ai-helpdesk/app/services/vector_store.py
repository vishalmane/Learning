import math
from dataclasses import dataclass
from typing import Iterable

from app.config import get_settings


@dataclass
class RetrievedDocument:
    content: str
    source: str
    score: float
    metadata: dict


DEFAULT_DOCUMENTS = [
    RetrievedDocument(
        content="VPN MFA timeout is usually resolved by approving the push within 30 seconds, syncing device time, or resetting the authenticator registration.",
        source="kb://vpn/mfa-timeout",
        score=0.0,
        metadata={"category": "vpn"},
    ),
    RetrievedDocument(
        content="If VPN remains disconnected after MFA retry, collect client logs, network type, region, and last successful login time before escalating.",
        source="kb://vpn/escalation",
        score=0.0,
        metadata={"category": "vpn"},
    ),
    RetrievedDocument(
        content="Password resets, account deletion, account disablement, and access removal require manager or security approval before action.",
        source="kb://governance/sensitive-ops",
        score=0.0,
        metadata={"category": "governance"},
    ),
]


class VectorStore:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._docs = DEFAULT_DOCUMENTS

    def load_documents(self, docs: Iterable[tuple[str, str, dict]]) -> None:
        indexed = []
        for content, source, metadata in docs:
            for chunk in chunk_text(content):
                indexed.append(RetrievedDocument(content=chunk, source=source, score=0.0, metadata=metadata))
        self._docs = indexed or self._docs

    def retrieve_docs(self, query: str, top_k: int | None = None) -> list[dict]:
        top_k = top_k or self.settings.retrieval_top_k
        query_tokens = _tokens(query)
        ranked = []
        for doc in self._docs:
            score = _cosine(query_tokens, _tokens(doc.content))
            ranked.append(RetrievedDocument(doc.content, doc.source, score, doc.metadata))
        ranked.sort(key=lambda item: item.score, reverse=True)
        return [
            {"content": item.content, "source": item.source, "score": item.score, "metadata": item.metadata}
            for item in ranked[:top_k]
        ]


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        next_start = end - overlap
        start = next_start if next_start > start else end
    return chunks


def _tokens(text: str) -> dict[str, float]:
    counts: dict[str, float] = {}
    for token in text.lower().replace("/", " ").replace("-", " ").split():
        counts[token] = counts.get(token, 0.0) + 1.0
    return counts


def _cosine(left: dict[str, float], right: dict[str, float]) -> float:
    dot = sum(left.get(key, 0.0) * right.get(key, 0.0) for key in left)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)
