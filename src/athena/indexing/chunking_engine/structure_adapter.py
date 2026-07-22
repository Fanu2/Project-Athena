"""
Structure-aware chunking adapter.

Wraps ChunkingEngine so it can be used by IndexingService
through the common ChunkingAdapter interface.
"""

from __future__ import annotations

from athena.indexing.chunking_engine.adapter import (
    ChunkingAdapter,
)
from athena.indexing.chunking_engine.engine import (
    ChunkingEngine,
)
from athena.indexing.models import (
    DocumentChunk,
    ExtractedDocument,
)


class StructureChunkingAdapter(ChunkingAdapter):
    """
    Adapter for the new structure-aware chunking engine.
    """

    def __init__(
        self,
        engine: ChunkingEngine | None = None,
    ) -> None:
        self._engine = (
            engine
            if engine is not None
            else ChunkingEngine()
        )

    def chunk_document(
        self,
        document: ExtractedDocument,
        document_id: str | None = None,
    ) -> list[DocumentChunk]:
        """
        Convert an extracted document into searchable chunks.
        """

        chunks = self._engine.process(
            document,
        )

        if document_id is None:
            return chunks

        return [
            DocumentChunk(
                chunk_id=chunk.chunk_id,
                document_id=document_id,
                chunk_index=chunk.chunk_index,
                page_number=chunk.page_number,
                start_offset=chunk.start_offset,
                end_offset=chunk.end_offset,
                text=chunk.text,
                heading=chunk.heading,
                heading_path=chunk.heading_path,
                chunk_type=chunk.chunk_type,
                previous_chunk=chunk.previous_chunk,
                next_chunk=chunk.next_chunk,
            )
            for chunk in chunks
        ]