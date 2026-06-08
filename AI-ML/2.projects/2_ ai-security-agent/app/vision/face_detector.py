"""Face detection service using RetinaFace."""

from typing import Any

from app.config.settings import get_settings


class FaceDetector:
    """Detects faces in camera frames."""

    def __init__(self) -> None:
        self.settings = get_settings()

    def detect_faces(self, frame: Any) -> list[dict[str, Any]]:
        """Return detected face bounding boxes and confidence scores for a frame."""
        from deepface import DeepFace

        detected_faces = DeepFace.extract_faces(
            img_path=frame,
            detector_backend="retinaface",
            enforce_detection=False,
            align=False,
        )

        faces: list[dict[str, Any]] = []
        for detected_face in detected_faces:
            area = detected_face.get("facial_area", {})
            faces.append(
                {
                    "x": int(area.get("x", 0)),
                    "y": int(area.get("y", 0)),
                    "w": int(area.get("w", 0)),
                    "h": int(area.get("h", 0)),
                    "confidence": float(detected_face.get("confidence", 0.0)),
                }
            )

        return faces
