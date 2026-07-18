"""
SQLite chunk repository.
"""

from __future__ import annotations

from athena.indexing.models import DocumentChunk
from athena.indexing.repositories.base import ChunkRepository


class SQLiteChunkRepository(ChunkRepository):
    """SQLite-backed repository."""

    def save_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> None:
        raise NotImplementedError

    def load_chunks(
        self,
        document_id: str,
    ) -> list[DocumentChunk]:
        raise NotImplementedError

    def delete_chunks(
        self,
        document_id: str,
    ) -> None:
        raise NotImplementedError
