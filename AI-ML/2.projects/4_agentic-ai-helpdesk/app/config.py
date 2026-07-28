from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Agentic AI Helpdesk Assistant"
    environment: Literal["local", "test", "production"] = "local"
    log_level: str = "INFO"

    llm_provider: Literal["gemini", "openai", "fallback"] = "gemini"

    google_api_key: str | None = Field(default=None, validation_alias="GOOGLE_API_KEY")
    gemini_api_key: str | None = Field(default=None, validation_alias="GEMINI_API_KEY")
    gemini_model: str = "gemini-2.5-flash"

    openai_api_key: str | None = Field(default=None, validation_alias="OPENAI_API_KEY")
    openai_model: str = "gpt-4o-mini"
    embedding_provider: Literal["gemini", "openai", "fallback"] = "gemini"
    gemini_embedding_model: str = "models/text-embedding-004"
    openai_embedding_model: str = "text-embedding-3-small"

    database_url: str = "postgresql+psycopg://helpdesk:helpdesk@postgres:5432/helpdesk"
    redis_url: str = "redis://redis:6379/0"
    redis_ttl_seconds: int = 86_400

    retrieval_top_k: int = 4
    max_query_length: int = 4_000
    rate_limit_per_minute: int = 60
    enable_llm_governance: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
