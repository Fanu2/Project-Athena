"""
Legacy chunking adapter.

Wraps the existing ChunkingService so it can be used through
the common ChunkingAdapter interface.
"""

from __future__ import annotations

from athena.indexing.chunking import ChunkingService
from athena.indexing.chunking_engine.adapter import (
    ChunkingAdapter,
)
from athena.indexing.models import (
    DocumentChunk,
    ExtractedDocument,
)


class LegacyChunkingAdapter(ChunkingAdapter):
    """
    Adapter for the existing chunking implementation.
    """

    def __init__(
        self,
        chunking_service: ChunkingService | None = None,
    ) -> None:
        self._chunking_service = (
            chunking_service
            if chunking_service is not None
            else ChunkingService()
        )

    def chunk_document(
        self,
        document: ExtractedDocument,
        document_id: str | None = None,
    ) -> list[DocumentChunk]:
        """
        Generate chunks using the legacy chunker.
        """

        return self._chunking_service.chunk_document(
            document,
            document_id=document_id,
        )