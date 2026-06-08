"""Vector memory placeholder for face embeddings."""


class FaceVectorStore:
    """Stores and searches face embeddings."""

    def add_embedding(self, identity: str, embedding: list[float]) -> None:
        """Add a face embedding for an identity."""
        _ = (identity, embedding)

    def search(self, embedding: list[float]) -> list[dict[str, float | str]]:
        """Search for similar face embeddings."""
        _ = embedding
        return []
