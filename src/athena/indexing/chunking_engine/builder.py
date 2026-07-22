"""
Chunk builder.

Combines DocumentBlocks into ChunkCandidates while preserving
document structure and respecting maximum chunk size.
"""

from __future__ import annotations

from athena.indexing.chunking_engine.models import (
    BlockType,
    ChunkCandidate,
    ChunkType,
    DocumentBlock,
)


class ChunkBuilder:
    """
    Builds ChunkCandidates from a sequence of DocumentBlocks.

    The builder is responsible only for grouping structural blocks into
    logical chunks. It does not create metadata or final DocumentChunk
    instances.
    """

    def __init__(
        self,
        max_characters: int = 1200,
    ) -> None:
        self._max_characters = max_characters

    def build(
        self,
        blocks: list[DocumentBlock],
    ) -> list[ChunkCandidate]:
        """
        Assemble blocks into chunk candidates.
        """

        if not blocks:
            return []

        chunks: list[ChunkCandidate] = []
        current = ChunkCandidate()

        for block in blocks:

            projected_length = len(current.text)

            if current.text:
                projected_length += 2  # separator

            projected_length += len(block.text)

            if (
                current.blocks
                and projected_length > self._max_characters
            ):
                chunks.append(current)
                current = ChunkCandidate()

            self._append_block(current, block)

        if current.blocks:
            chunks.append(current)

        return chunks

    @staticmethod
    def _append_block(
        chunk: ChunkCandidate,
        block: DocumentBlock,
    ) -> None:
        """
        Append a DocumentBlock to a ChunkCandidate.
        """

        chunk.blocks.append(block)

        if chunk.text:
            chunk.text += "\n\n"

        chunk.text += block.text

        if len(chunk.blocks) == 1:
            chunk.page_number = block.page_number
            chunk.heading = block.heading
            chunk.heading_path = block.heading_path

        chunk.chunk_type = ChunkBuilder._determine_chunk_type(chunk)

    @staticmethod
    def _determine_chunk_type(
        chunk: ChunkCandidate,
    ) -> ChunkType:
        """
        Determine the logical type of a chunk.
        """

        if not chunk.blocks:
            return ChunkType.PARAGRAPH

        block_types = {
            block.block_type
            for block in chunk.blocks
        }

        if len(block_types) > 1:
            return ChunkType.MIXED

        block_type = next(iter(block_types))

        mapping = {
            BlockType.HEADING: ChunkType.HEADING,
            BlockType.PARAGRAPH: ChunkType.PARAGRAPH,
            BlockType.LIST: ChunkType.LIST,
            BlockType.TABLE: ChunkType.TABLE,
            BlockType.CODE: ChunkType.CODE,
        }

        return mapping.get(block_type, ChunkType.MIXED)