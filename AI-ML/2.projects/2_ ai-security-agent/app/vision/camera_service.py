"""Camera capture service for reading frames from a camera source."""

from threading import Event
from time import perf_counter, sleep
from typing import Any

import cv2

from app.config.settings import get_settings
from app.recognition.face_recognizer import FaceRecognizer
from app.vision.face_detector import FaceDetector


class CameraService:
    """Manages camera source configuration and frame capture."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.capture: cv2.VideoCapture | None = None

    def get_camera_source(self) -> int | str:
        """Return the configured camera source."""
        source = self.settings.camera_source
        return int(source) if source.isdigit() else source

    def open(self) -> None:
        """Open the configured camera source."""
        if self.capture is not None and self.capture.isOpened():
            return

        self.capture = cv2.VideoCapture(self.get_camera_source())
        if not self.capture.isOpened():
            self.capture.release()
            self.capture = None
            raise RuntimeError(f"Unable to open camera source: {self.settings.camera_source}")

    def read_frame(self) -> Any:
        """Read a frame from the camera source."""
        self.open()
        if self.capture is None:
            raise RuntimeError("Camera is not initialized")

        success, frame = self.capture.read()
        if not success or frame is None:
            raise RuntimeError("Unable to read frame from camera")

        return frame

    def release(self) -> None:
        """Release the active camera capture."""
        if self.capture is not None:
            self.capture.release()
            self.capture = None

    def __enter__(self) -> "CameraService":
        """Open the camera when used as a context manager."""
        self.open()
        return self

    def __exit__(self, *_: object) -> None:
        """Release the camera when leaving a context manager."""
        self.release()


def draw_face_boxes(frame: Any, faces: list[dict[str, Any]]) -> Any:
    """Draw face detection and recognition labels on a camera frame."""
    for face in faces:
        x = int(face["x"])
        y = int(face["y"])
        w = int(face["w"])
        h = int(face["h"])
        confidence = float(face["confidence"])
        identity = face.get("identity")
        recognition_confidence = face.get("recognition_confidence")
        label = f"Face {confidence:.2f}"

        if identity:
            label = f"{identity} {float(recognition_confidence or 0.0):.2f}"
        elif face.get("recognized") is False:
            label = "Unknown"

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            label,
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

    return frame


def crop_face(frame: Any, face: dict[str, Any], padding_ratio: float = 0.2) -> Any | None:
    """Return a padded face crop from a camera frame."""
    frame_height, frame_width = frame.shape[:2]
    x = int(face["x"])
    y = int(face["y"])
    w = int(face["w"])
    h = int(face["h"])
    padding = int(max(w, h) * padding_ratio)

    x1 = max(0, x - padding)
    y1 = max(0, y - padding)
    x2 = min(frame_width, x + w + padding)
    y2 = min(frame_height, y + h + padding)

    if x1 >= x2 or y1 >= y2:
        return None

    return frame[y1:y2, x1:x2].copy()


def recognize_faces(
    frame: Any,
    faces: list[dict[str, Any]],
    recognizer: FaceRecognizer,
) -> list[dict[str, Any]]:
    """Recognize detected face crops against enrolled people."""
    known_embeddings = recognizer.load_known_embeddings()
    recognized_faces: list[dict[str, Any]] = []

    for face in faces:
        face_with_result = face.copy()
        if not known_embeddings:
            face_with_result["recognized"] = False
            recognized_faces.append(face_with_result)
            continue

        face_crop = crop_face(frame, face)
        if face_crop is None:
            face_with_result["recognized"] = False
            recognized_faces.append(face_with_result)
            continue

        result = recognizer.recognize(face_crop, known_embeddings=known_embeddings)
        face_with_result["identity"] = result.get("identity")
        face_with_result["recognition_confidence"] = float(result.get("confidence", 0.0))
        face_with_result["recognized"] = result.get("identity") is not None
        recognized_faces.append(face_with_result)

    return recognized_faces


def preview_camera(stop_event: Event | None = None) -> None:
    """Show a local preview window for the configured camera feed."""
    settings = get_settings()
    camera = CameraService()
    detector = FaceDetector()
    recognizer = FaceRecognizer()
    faces: list[dict[str, Any]] = []
    frame_count = 0
    detection_interval = max(1, settings.face_detection_interval)
    target_fps = max(1.0, settings.camera_target_fps)
    frame_interval_seconds = 1.0 / target_fps
    window_name = "AI Security Agent - Camera Feed"

    try:
        while stop_event is None or not stop_event.is_set():
            frame_started_at = perf_counter()
            frame = camera.read_frame()
            frame_count += 1

            if frame_count % detection_interval == 0:
                faces = detector.detect_faces(frame)
                faces = recognize_faces(frame, faces, recognizer)

            draw_face_boxes(frame, faces)
            cv2.imshow(window_name, frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            elapsed_seconds = perf_counter() - frame_started_at
            sleep_seconds = frame_interval_seconds - elapsed_seconds
            if sleep_seconds > 0:
                sleep(sleep_seconds)
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    preview_camera()
