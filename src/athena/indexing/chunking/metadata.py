"""
Metadata builder.

Converts ChunkCandidates into final DocumentChunks.
"""

from __future__ import annotations

import uuid

from athena.indexing.models import DocumentChunk

from athena.indexing.chunking.models import ChunkCandidate


class MetadataBuilder:
    """
    Converts ChunkCandidates into searchable DocumentChunks.
    """

    def build(
        self,
        document_id: str,
        candidates: list[ChunkCandidate],
    ) -> list[DocumentChunk]:
        """
        Build final searchable chunks.
        """

        chunks: list[DocumentChunk] = []

        previous_chunk_id: str | None = None

        for index, candidate in enumerate(candidates):
            chunk_id = str(uuid.uuid4())

            start_offset = candidate.blocks[0].start_offset
            end_offset = candidate.blocks[-1].end_offset

            chunk = DocumentChunk(
                chunk_id=chunk_id,
                document_id=document_id,
                chunk_index=index,
                page_number=candidate.page_number,
                start_offset=start_offset,
                end_offset=end_offset,
                text=candidate.text,
                heading=candidate.heading,
                heading_path=candidate.heading_path,
                chunk_type=candidate.chunk_type,
                previous_chunk=previous_chunk_id,
                next_chunk=None,
            )

            chunks.append(chunk)

            previous_chunk_id = chunk_id

        #
        # Link forward references
        #

        for index in range(len(chunks) - 1):
            current = chunks[index]
            nxt = chunks[index + 1]

            chunks[index] = DocumentChunk(
                chunk_id=current.chunk_id,
                document_id=current.document_id,
                chunk_index=current.chunk_index,
                page_number=current.page_number,
                start_offset=current.start_offset,
                end_offset=current.end_offset,
                text=current.text,
                heading=current.heading,
                heading_path=current.heading_path,
                chunk_type=current.chunk_type,
                previous_chunk=current.previous_chunk,
                next_chunk=nxt.chunk_id,
            )

        return chunks
