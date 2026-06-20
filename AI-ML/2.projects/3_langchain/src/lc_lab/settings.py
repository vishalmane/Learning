from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    model: str = "gemini-2.5-flash"
    embedding_model: str = "gemini-embedding-2-preview"
    temperature: float = 0.2


def load_settings() -> Settings:
    load_dotenv()
    return Settings(
        model=os.getenv("LC_LAB_MODEL", "gemini-2.5-flash"),
        embedding_model=os.getenv("LC_LAB_EMBEDDING_MODEL", "gemini-embedding-2-preview"),
        temperature=float(os.getenv("LC_LAB_TEMPERATURE", "0.2")),
    )
