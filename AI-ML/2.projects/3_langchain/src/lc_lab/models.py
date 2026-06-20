from __future__ import annotations

from langchain_google_genai import ChatGoogleGenerativeAI

from lc_lab.settings import load_settings


def get_chat_model(model: str | None = None, temperature: float | None = None):
    settings = load_settings()
    return ChatGoogleGenerativeAI(
        model=model or settings.model,
        temperature=settings.temperature if temperature is None else temperature,
    )
