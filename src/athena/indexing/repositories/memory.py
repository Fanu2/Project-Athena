"""
In-memory chunk repository.
"""

from __future__ import annotations

from athena.indexing.models import DocumentChunk
from athena.indexing.repositories.base import ChunkRepository


class MemoryChunkRepository(ChunkRepository):
    """Store document chunks in memory."""

    def __init__(self) -> None:
        self._storage: dict[str, list[DocumentChunk]] = {}

    def save_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> None:
        if not chunks:
            return

        self._storage[chunks[0].document_id] = list(chunks)

    def load_chunks(
        self,
        document_id: str,
    ) -> list[DocumentChunk]:
        return list(
            self._storage.get(
                document_id,
                [],
            )
        )

    def delete_chunks(
        self,
        document_id: str,
    ) -> None:
        self._storage.pop(
            document_id,
            None,
        )
