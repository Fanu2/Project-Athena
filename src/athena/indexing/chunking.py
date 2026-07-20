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
        document_id: str | None = None,
    ) -> list[DocumentChunk]:
        """
        Split an extracted document into searchable chunks.

        Parameters
        ----------
        document:
            Extracted document.

        document_id:
            Optional external document identifier.
            When provided, chunks will use this ID instead
            of the extractor-generated ID.
        """

        chunks: list[DocumentChunk] = []

        chunk_document_id = (
            document_id
            if document_id is not None
            else document.document_id
        )

        chunk_index = 0

        for page in document.pages:

            text = page.text

            if not text.strip():
                continue

            start = 0

            while start < len(text):

                end = min(
                    start + self._chunk_size,
                    len(text),
                )

                chunk_text = text[start:end]

                chunks.append(
                    DocumentChunk(
                        chunk_id=f"{chunk_document_id}:{chunk_index}",
                        document_id=chunk_document_id,
                        chunk_index=chunk_index,
                        page_number=page.page_number,
                        start_offset=start,
                        end_offset=end,
                        text=chunk_text,
                    )
                )

                chunk_index += 1

                if end == len(text):
                    break

                start = end - self._overlap

        return chunks