"""
Chunk repository interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from athena.indexing.models import DocumentChunk


class ChunkRepository(ABC):
    """Abstract repository for document chunks."""

    @abstractmethod
    def save_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> None:
        """Save chunks."""

    @abstractmethod
    def load_chunks(
        self,
        document_id: str,
    ) -> list[DocumentChunk]:
        """Load chunks."""

    @abstractmethod
    def delete_chunks(
        self,
        document_id: str,
    ) -> None:
        """Delete chunks."""
