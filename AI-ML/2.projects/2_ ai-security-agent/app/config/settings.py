"""Application settings loaded from environment variables."""

import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()


class Settings(BaseModel):
    """Runtime configuration for the AI Security Agent."""

    app_name: str = os.getenv("APP_NAME", "ai-security-agent")
    app_env: str = os.getenv("APP_ENV", "development")
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app/database/ai_security_agent.db")
    camera_source: str = os.getenv("CAMERA_SOURCE", "0")
    face_detection_backend: str = os.getenv("FACE_DETECTION_BACKEND", "opencv")
    face_recognition_model: str = os.getenv("FACE_RECOGNITION_MODEL", "Facenet")
    face_match_threshold: float = float(os.getenv("FACE_MATCH_THRESHOLD", "0.65"))


@lru_cache
def get_settings() -> Settings:
    """Return cached settings for use across the application."""
    return Settings()
