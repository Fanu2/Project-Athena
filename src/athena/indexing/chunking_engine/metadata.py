"""
Metadata builder.

Converts ChunkCandidate objects into DocumentChunk instances ready
for indexing. This stage enriches chunks with stable identifiers and
document-level metadata but does not generate embeddings.
"""

from __future__ import annotations

from uuid import uuid4

from athena.indexing.chunking_engine.models import (
    ChunkCandidate,
)
from athena.indexing.models import (
    DocumentChunk,
    ExtractedDocument,
)


class MetadataBuilder:
    """
    Converts ChunkCandidates into DocumentChunks.
    """

    def build(
        self,
        document: ExtractedDocument,
        candidates: list[ChunkCandidate],
    ) -> list[DocumentChunk]:
        """
        Build DocumentChunk objects ready for indexing.
        """

        chunks: list[DocumentChunk] = []

        total_chunks = len(candidates)

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
                    text=candidate.text,
                    page_number=candidate.page_number,
                    start_offset=start_offset,
                    end_offset=end_offset,
                    heading=candidate.heading,
                    heading_path=candidate.heading_path,
                    chunk_type=candidate.chunk_type,
                    chunk_index=index,
                    chunk_count=total_chunks,
                )
            )

        return chunks