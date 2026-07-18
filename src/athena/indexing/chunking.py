"""
Document chunking.
"""

from __future__ import annotations

from athena.indexing.constants import (
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_CHUNK_SIZE,
)
from athena.indexing.models import (
    DocumentChunk,
    ExtractedDocument,
)


class ChunkingService:
    """Split extracted documents into searchable chunks."""

    def __init__(
        self,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        overlap: int = DEFAULT_CHUNK_OVERLAP,
    ) -> None:
        """Initialize the chunking service."""

        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive.")

        if overlap < 0:
            raise ValueError("overlap cannot be negative.")

        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size.")

        self._chunk_size = chunk_size
        self._overlap = overlap

    def chunk_document(
        self,
        document: ExtractedDocument,
    ) -> list[DocumentChunk]:
        """
        Split an extracted document into chunks.
        """

        text = document.text

        if not text.strip():
            return []

        chunks: list[DocumentChunk] = []

        start = 0
        index = 0

        while start < len(text):

            end = min(
                start + self._chunk_size,
                len(text),
            )

            chunk_text = text[start:end]

            chunks.append(
                DocumentChunk(
                    chunk_id=f"{document.document_id}:{index}",
                    document_id=document.document_id,
                    chunk_index=index,
                    page_number=1,
                    text=chunk_text,
                )
            )

            if end == len(text):
                break

            start = end - self._overlap
            index += 1

        return chunks
