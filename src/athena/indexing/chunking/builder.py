"""
Chunk builder.

Groups DocumentBlocks into ChunkCandidates.
"""

from __future__ import annotations

from athena.indexing.chunking.models import (
    BlockType,
    ChunkCandidate,
    ChunkType,
    DocumentBlock,
)


class ChunkBuilder:
    """
    Builds logical chunks from structural blocks.

    Responsibilities
    ----------------
    - Combine adjacent blocks.
    - Respect maximum chunk size.
    - Preserve headings.
    """

    def __init__(
        self,
        max_chars: int = 1000,
    ) -> None:
        self._max_chars = max_chars

    def build(
        self,
        blocks: list[DocumentBlock],
    ) -> list[ChunkCandidate]:
        """
        Build ChunkCandidates from DocumentBlocks.
        """

        if not blocks:
            return []

        chunks: list[ChunkCandidate] = []

        current = ChunkCandidate()

        for block in blocks:
            if current.blocks and len(current.text) + len(block.text) > self._max_chars:
                chunks.append(current)
                current = ChunkCandidate()

            if not current.blocks:
                current.page_number = block.page_number
                current.heading = block.heading
                current.heading_path = block.heading_path
                current.chunk_type = self._map_chunk_type(block.block_type)

            current.blocks.append(block)

            if current.text:
                current.text += "\n\n"

            current.text += block.text

        if current.blocks:
            chunks.append(current)

        return chunks

    @staticmethod
    def _map_chunk_type(
        block_type: BlockType,
    ) -> ChunkType:
        """
        Convert BlockType to ChunkType.
        """

        mapping = {
            BlockType.HEADING: ChunkType.HEADING,
            BlockType.PARAGRAPH: ChunkType.PARAGRAPH,
            BlockType.LIST: ChunkType.LIST,
            BlockType.TABLE: ChunkType.TABLE,
            BlockType.CODE: ChunkType.CODE,
        }

        return mapping.get(
            block_type,
            ChunkType.MIXED,
        )
