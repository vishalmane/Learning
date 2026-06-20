"""Face recognition service using DeepFace with RetinaFace detection."""

import argparse
import json
import re
import shutil
from math import sqrt
from pathlib import Path
from typing import Any, Mapping, Sequence

from app.config.settings import get_settings

KnownEmbeddings = Mapping[str, Sequence[float] | Sequence[Sequence[float]]]


class FaceRecognizer:
    """Recognizes faces from images or detected face crops."""

    detector_backend = "retinaface"
    supported_image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

    def __init__(self) -> None:
        self.settings = get_settings()

    def recognize(
        self,
        face_image: Any,
        known_embeddings: KnownEmbeddings | None = None,
    ) -> dict[str, Any]:
        """Return a recognition result for a face image.

        If `known_embeddings` is not supplied, enrolled embeddings are loaded
        from the local registry built by `enroll_person`.
        """
        representation = self.extract_embedding(face_image)
        if representation is None:
            return self._unknown_result(confidence=0.0, embedding=None, facial_area=None)

        embedding = representation["embedding"]
        facial_area = representation.get("facial_area")
        embeddings_to_search = known_embeddings if known_embeddings is not None else self.load_known_embeddings()
        best_match = self._find_best_match(embedding, embeddings_to_search)

        if best_match is None or best_match["confidence"] < self.settings.face_match_threshold:
            return self._unknown_result(
                confidence=best_match["confidence"] if best_match else 0.0,
                embedding=embedding,
                facial_area=facial_area,
            )

        return {
            "identity": best_match["identity"],
            "confidence": best_match["confidence"],
            "model": self.settings.face_recognition_model,
            "detector_backend": self.detector_backend,
            "embedding": embedding,
            "facial_area": facial_area,
        }

    def enroll_person(
        self,
        identity: str,
        image_paths: Sequence[str | Path],
    ) -> dict[str, Any]:
        """Add person photos to the local known-faces folder and embedding registry."""
        identity_name = self._sanitize_identity(identity)
        source_paths = [Path(image_path).expanduser() for image_path in image_paths]
        if not source_paths:
            raise ValueError("At least one face photo is required for enrollment")

        person_dir = self._person_dir(identity_name)
        person_dir.mkdir(parents=True, exist_ok=True)

        records = self._load_embedding_records()
        person_records = records.setdefault(identity_name, [])
        added_images: list[str] = []

        for source_path in source_paths:
            self._validate_image_path(source_path)
            destination = self._unique_destination(person_dir, source_path)
            shutil.copy2(source_path, destination)

            image_record = self._build_embedding_record(destination)
            if image_record is None:
                raise ValueError(f"No face embedding could be extracted from {destination}")

            person_records.append(image_record)
            added_images.append(str(destination))

        self._save_embedding_records(records)

        return {
            "identity": identity_name,
            "folder": str(person_dir),
            "images_added": added_images,
            "embedding_count": len(person_records),
        }

    def rebuild_embedding_registry(self) -> dict[str, Any]:
        """Rebuild embeddings from photos already stored in the known-faces folder."""
        records: dict[str, list[dict[str, Any]]] = {}
        indexed_images: list[str] = []
        skipped_images: list[str] = []

        self._known_faces_dir().mkdir(parents=True, exist_ok=True)

        for image_path in self._iter_known_face_images():
            identity_name = self._sanitize_identity(image_path.parent.name)
            image_record = self._build_embedding_record(image_path)
            if image_record is None:
                skipped_images.append(str(image_path))
                continue

            records.setdefault(identity_name, []).append(image_record)
            indexed_images.append(str(image_path))

        self._save_embedding_records(records)

        return {
            "people_count": len(records),
            "images_indexed": len(indexed_images),
            "images_skipped": skipped_images,
            "embeddings_path": str(self._embeddings_path()),
        }

    def load_known_embeddings(self) -> dict[str, list[list[float]]]:
        """Load enrolled face embeddings grouped by identity."""
        records = self._load_embedding_records()
        known_embeddings: dict[str, list[list[float]]] = {}

        for identity, person_records in records.items():
            embeddings = []
            for record in person_records:
                embedding = record.get("embedding")
                if isinstance(embedding, list):
                    embeddings.append([float(value) for value in embedding])

            if embeddings:
                known_embeddings[identity] = embeddings

        return known_embeddings

    def list_enrolled_people(self) -> list[dict[str, str | int]]:
        """Return enrolled identities and their saved photo counts."""
        records = self._load_embedding_records()
        return [
            {
                "identity": identity,
                "folder": str(self._person_dir(identity)),
                "image_count": len(person_records),
            }
            for identity, person_records in sorted(records.items())
        ]

    def extract_embedding(self, face_image: Any) -> dict[str, Any] | None:
        """Extract a DeepFace embedding using RetinaFace detection and alignment."""
        from deepface import DeepFace

        representations = DeepFace.represent(
            img_path=face_image,
            model_name=self.settings.face_recognition_model,
            detector_backend=self.detector_backend,
            enforce_detection=False,
            align=True,
        )

        if isinstance(representations, dict):
            representations = [representations]

        if not representations:
            return None

        valid_representations = [
            item for item in representations if isinstance(item.get("embedding"), list)
        ]
        if not valid_representations:
            return None

        strongest_face = max(
            valid_representations,
            key=lambda item: float(item.get("face_confidence", item.get("confidence", 0.0))),
        )

        return {
            "embedding": [float(value) for value in strongest_face["embedding"]],
            "facial_area": strongest_face.get("facial_area"),
            "face_confidence": float(
                strongest_face.get("face_confidence", strongest_face.get("confidence", 0.0))
            ),
        }

    def verify(self, first_face_image: Any, second_face_image: Any) -> dict[str, Any]:
        """Verify whether two face images belong to the same identity."""
        from deepface import DeepFace

        result = DeepFace.verify(
            img1_path=first_face_image,
            img2_path=second_face_image,
            model_name=self.settings.face_recognition_model,
            detector_backend=self.detector_backend,
            enforce_detection=False,
            align=True,
        )

        return {
            "verified": bool(result.get("verified", False)),
            "distance": float(result.get("distance", 1.0)),
            "threshold": float(result.get("threshold", self.settings.face_match_threshold)),
            "model": self.settings.face_recognition_model,
            "detector_backend": self.detector_backend,
        }

    def _unknown_result(
        self,
        confidence: float,
        embedding: list[float] | None,
        facial_area: dict[str, Any] | None,
    ) -> dict[str, Any]:
        """Build a consistent result for an unknown or undetected face."""
        return {
            "identity": None,
            "confidence": confidence,
            "model": self.settings.face_recognition_model,
            "detector_backend": self.detector_backend,
            "embedding": embedding,
            "facial_area": facial_area,
        }

    def _find_best_match(
        self,
        embedding: Sequence[float],
        known_embeddings: KnownEmbeddings,
    ) -> dict[str, str | float] | None:
        """Find the closest known embedding by cosine similarity."""
        best_identity: str | None = None
        best_confidence = 0.0

        for identity, known_embedding in self._iter_known_embeddings(known_embeddings):
            confidence = self._cosine_similarity(embedding, known_embedding)
            if confidence > best_confidence:
                best_identity = identity
                best_confidence = confidence

        if best_identity is None:
            return None

        return {
            "identity": best_identity,
            "confidence": best_confidence,
        }

    def _iter_known_embeddings(
        self,
        known_embeddings: KnownEmbeddings,
    ) -> list[tuple[str, Sequence[float]]]:
        """Flatten one or many embeddings per identity into searchable pairs."""
        searchable_embeddings: list[tuple[str, Sequence[float]]] = []

        for identity, embeddings in known_embeddings.items():
            if self._is_embedding(embeddings):
                searchable_embeddings.append((identity, embeddings))
                continue

            for embedding in embeddings:
                if self._is_embedding(embedding):
                    searchable_embeddings.append((identity, embedding))

        return searchable_embeddings

    def _load_embedding_records(self) -> dict[str, list[dict[str, Any]]]:
        """Load the persisted embedding registry."""
        embeddings_path = self._embeddings_path()
        if not embeddings_path.exists():
            return {}

        with embeddings_path.open("r", encoding="utf-8") as file:
            payload = json.load(file)

        people = payload.get("people", {})
        if not isinstance(people, dict):
            return {}

        return {
            str(identity): person_records
            for identity, person_records in people.items()
            if isinstance(person_records, list)
        }

    def _save_embedding_records(self, records: dict[str, list[dict[str, Any]]]) -> None:
        """Persist the embedding registry."""
        embeddings_path = self._embeddings_path()
        embeddings_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": 1,
            "model": self.settings.face_recognition_model,
            "detector_backend": self.detector_backend,
            "people": records,
        }

        with embeddings_path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)

    def _build_embedding_record(self, image_path: Path) -> dict[str, Any] | None:
        """Build one persisted embedding record for a known face photo."""
        representation = self.extract_embedding(str(image_path))
        if representation is None:
            return None

        return {
            "image_path": str(image_path),
            "embedding": representation["embedding"],
            "facial_area": representation.get("facial_area"),
            "face_confidence": representation.get("face_confidence", 0.0),
            "model": self.settings.face_recognition_model,
            "detector_backend": self.detector_backend,
        }

    def _known_faces_dir(self) -> Path:
        """Return the configured known-faces photo directory."""
        return Path(self.settings.known_faces_dir).expanduser()

    def _embeddings_path(self) -> Path:
        """Return the configured embedding registry path."""
        return Path(self.settings.face_embeddings_path).expanduser()

    def _person_dir(self, identity: str) -> Path:
        """Return the folder for an enrolled identity."""
        return self._known_faces_dir() / self._sanitize_identity(identity)

    def _unique_destination(self, person_dir: Path, source_path: Path) -> Path:
        """Return a non-conflicting destination path for an enrollment photo."""
        file_stem = self._sanitize_file_stem(source_path.stem)
        suffix = source_path.suffix.lower()
        candidate = person_dir / f"{file_stem}{suffix}"
        counter = 1

        while candidate.exists():
            candidate = person_dir / f"{file_stem}_{counter}{suffix}"
            counter += 1

        return candidate

    def _iter_known_face_images(self) -> list[Path]:
        """Return image files already placed in the known-faces folder."""
        known_faces_dir = self._known_faces_dir()
        if not known_faces_dir.exists():
            return []

        return sorted(
            image_path
            for image_path in known_faces_dir.rglob("*")
            if image_path.is_file()
            and image_path.suffix.lower() in self.supported_image_extensions
        )

    def _validate_image_path(self, image_path: Path) -> None:
        """Validate that an enrollment image can be copied and processed."""
        if not image_path.exists():
            raise FileNotFoundError(f"Face photo does not exist: {image_path}")
        if not image_path.is_file():
            raise ValueError(f"Face photo path must be a file: {image_path}")
        if image_path.suffix.lower() not in self.supported_image_extensions:
            supported = ", ".join(sorted(self.supported_image_extensions))
            raise ValueError(f"Unsupported face photo type {image_path.suffix}. Use: {supported}")

    @staticmethod
    def _sanitize_identity(identity: str) -> str:
        """Convert a display name into a safe folder name."""
        cleaned = re.sub(r"[^A-Za-z0-9_. -]+", "_", identity.strip()).strip(" ._")
        if not cleaned:
            raise ValueError("Identity must contain at least one letter or number")
        return cleaned

    @staticmethod
    def _sanitize_file_stem(file_stem: str) -> str:
        """Convert an uploaded file name into a safe stored file name."""
        cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", file_stem.strip()).strip("._")
        return cleaned or "face"

    @staticmethod
    def _is_embedding(value: object) -> bool:
        """Return whether a value looks like a single numeric embedding."""
        return isinstance(value, Sequence) and bool(value) and all(
            isinstance(item, int | float) for item in value
        )

    @staticmethod
    def _cosine_similarity(
        first_embedding: Sequence[float],
        second_embedding: Sequence[float],
    ) -> float:
        """Return cosine similarity normalized to the range 0.0 to 1.0."""
        if len(first_embedding) != len(second_embedding):
            return 0.0

        dot_product = sum(
            first * second for first, second in zip(first_embedding, second_embedding)
        )
        first_norm = sqrt(sum(value * value for value in first_embedding))
        second_norm = sqrt(sum(value * value for value in second_embedding))

        if first_norm == 0.0 or second_norm == 0.0:
            return 0.0

        return max(0.0, min(1.0, dot_product / (first_norm * second_norm)))


def _result_without_embedding(result: dict[str, Any]) -> dict[str, Any]:
    """Return CLI-friendly output without printing the full embedding vector."""
    output = result.copy()
    embedding = output.pop("embedding", None)
    output["embedding_dimensions"] = len(embedding) if isinstance(embedding, list) else 0
    return output


def main() -> None:
    """Run simple enrollment and recognition commands from the terminal."""
    parser = argparse.ArgumentParser(description="Enroll and recognize known faces.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    enroll_parser = subparsers.add_parser("enroll", help="Add photos for a known person.")
    enroll_parser.add_argument("identity", help="Person name, for example: Alice")
    enroll_parser.add_argument("images", nargs="+", help="One or more face photo paths.")

    recognize_parser = subparsers.add_parser(
        "recognize",
        help="Recognize a face image against enrolled people.",
    )
    recognize_parser.add_argument("image", help="Face image to recognize.")

    subparsers.add_parser("list", help="List enrolled people.")
    subparsers.add_parser(
        "rebuild",
        help="Rebuild embeddings from photos already in the known-faces folder.",
    )

    args = parser.parse_args()
    recognizer = FaceRecognizer()

    if args.command == "enroll":
        result = recognizer.enroll_person(args.identity, args.images)
    elif args.command == "recognize":
        result = _result_without_embedding(recognizer.recognize(args.image))
    elif args.command == "rebuild":
        result = recognizer.rebuild_embedding_registry()
    else:
        result = {"people": recognizer.list_enrolled_people()}

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
