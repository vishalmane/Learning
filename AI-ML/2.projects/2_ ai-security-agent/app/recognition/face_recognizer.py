"""Face recognition placeholder using DeepFace-compatible concepts."""

from app.config.settings import get_settings


class FaceRecognizer:
    """Recognizes faces from detected face crops."""

    def __init__(self) -> None:
        self.settings = get_settings()

    def recognize(self, face_image) -> dict[str, str | float | None]:
        """Return a placeholder recognition result for a face image."""
        _ = face_image
        return {
            "identity": None,
            "confidence": 0.0,
            "model": self.settings.face_recognition_model,
        }
