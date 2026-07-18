"""
In-memory chunk repository.
"""

from __future__ import annotations

from athena.indexing.models import DocumentChunk
from athena.indexing.repositories.base import ChunkRepository


class MemoryChunkRepository(ChunkRepository):
    """In-memory implementation of ChunkRepository."""

    def __init__(self) -> None:
        self._chunks: dict[str, list[DocumentChunk]] = {}

    def save_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> None:
        """Save document chunks."""
        if not chunks:
            return

        self._chunks[chunks[0].document_id] = list(chunks)

    def load_chunks(
        self,
        document_id: str,
    ) -> list[DocumentChunk]:
        """Load all chunks for a document."""
        return list(self._chunks.get(document_id, []))

    def delete_chunks(
        self,
        document_id: str,
    ) -> None:
        """Delete all chunks for a document."""
        self._chunks.pop(document_id, None)

    def search_chunks(
        self,
        query: str,
        limit: int = 20,
    ) -> list[DocumentChunk]:
        """
        Search indexed document chunks.

        Parameters
        ----------
        query:
            Search text.

        limit:
            Maximum number of results.

        Returns
        -------
        list[DocumentChunk]
            Matching document chunks.
        """
        query = query.lower()

        results: list[DocumentChunk] = []

        for chunks in self._chunks.values():
            for chunk in chunks:
                if query in chunk.text.lower():
                    results.append(chunk)

                    if len(results) >= limit:
                        return results

        return results
