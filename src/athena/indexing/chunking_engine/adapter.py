"""
Chunking adapter abstraction.

Provides a common interface so Athena can switch between
legacy chunking and the new structure-aware chunking engine
without changing IndexingService.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from athena.indexing.models import (
    DocumentChunk,
    ExtractedDocument,
)


class ChunkingAdapter(ABC):
    """
    Common interface for document chunking implementations.
    """

    @abstractmethod
    def chunk_document(
        self,
        document: ExtractedDocument,
        document_id: str | None = None,
    ) -> list[DocumentChunk]:
        """
        Convert an extracted document into searchable chunks.
        """

        raise NotImplementedError