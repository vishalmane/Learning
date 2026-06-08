"""Camera capture service for reading frames from a camera source."""

from threading import Event
from typing import Any

import cv2

from app.config.settings import get_settings
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
    """Draw face detection boxes on a camera frame."""
    for face in faces:
        x = int(face["x"])
        y = int(face["y"])
        w = int(face["w"])
        h = int(face["h"])
        confidence = float(face["confidence"])

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"Face {confidence:.2f}",
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

    return frame


def preview_camera(stop_event: Event | None = None) -> None:
    """Show a local preview window for the configured camera feed."""
    camera = CameraService()
    detector = FaceDetector()
    faces: list[dict[str, Any]] = []
    frame_count = 0
    detection_interval = 10
    window_name = "AI Security Agent - Camera Feed"

    try:
        while stop_event is None or not stop_event.is_set():
            frame = camera.read_frame()
            frame_count += 1

            if frame_count % detection_interval == 0:
                faces = detector.detect_faces(frame)

            draw_face_boxes(frame, faces)
            cv2.imshow(window_name, frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    preview_camera()
