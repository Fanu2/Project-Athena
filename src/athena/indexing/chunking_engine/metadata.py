"""
Metadata builder.

Converts ChunkCandidate objects into immutable DocumentChunk instances
ready for indexing. This stage enriches chunks with stable identifiers
and document metadata but does not generate embeddings.
"""

from __future__ import annotations

from uuid import uuid4

from athena.indexing.chunking_engine.models import ChunkCandidate
from athena.indexing.models import (
    DocumentChunk,
    ExtractedDocument,
)


class MetadataBuilder:
    """
    Builds immutable DocumentChunk objects from ChunkCandidates.
    """

    def build(
        self,
        document: ExtractedDocument,
        candidates: list[ChunkCandidate],
    ) -> list[DocumentChunk]:
        """
        Convert chunk candidates into final searchable chunks.
        """

        chunks: list[DocumentChunk] = []

        for index, candidate in enumerate(candidates):
            start_offset = (
                candidate.blocks[0].start_offset
                if candidate.blocks
                else 0
            )

            end_offset = (
                candidate.blocks[-1].end_offset
                if candidate.blocks
                else 0
            )

            chunks.append(
                DocumentChunk(
                    chunk_id=str(uuid4()),
                    document_id=document.document_id,
                    chunk_index=index,
                    page_number=candidate.page_number,
                    start_offset=start_offset,
                    end_offset=end_offset,
                    text=candidate.text,
                    heading=candidate.heading,
                    heading_path=candidate.heading_path,
                    chunk_type=candidate.chunk_type,
                )
            )

        return chunks