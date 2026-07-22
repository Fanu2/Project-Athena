"""
Structure-aware block splitter.

The splitter ensures that individual DocumentBlocks do not exceed the
configured maximum size while preserving document structure.

The splitter operates only on DocumentBlocks. It does not assemble
chunks; that responsibility belongs to ChunkBuilder.
"""

from __future__ import annotations

from athena.indexing.chunking_engine.models import DocumentBlock


class ChunkSplitter:
    """
    Splits oversized DocumentBlocks into smaller blocks.
    """

    def __init__(
        self,
        max_characters: int = 1000,
    ) -> None:
        self._max_characters = max_characters

    def split(
        self,
        blocks: list[DocumentBlock],
    ) -> list[DocumentBlock]:
        """
        Split oversized blocks while preserving order.
        """

        result: list[DocumentBlock] = []

        for block in blocks:

            if len(block.text) <= self._max_characters:
                result.append(block)
                continue

            result.extend(self._split_block(block))

        return result

    def _split_block(
        self,
        block: DocumentBlock,
    ) -> list[DocumentBlock]:
        """
        Split a single oversized block.
        """

        pieces: list[DocumentBlock] = []

        text = block.text

        start = 0

        while start < len(text):

            end = min(
                start + self._max_characters,
                len(text),
            )

            piece = text[start:end]

            pieces.append(
                DocumentBlock(
                    block_type=block.block_type,
                    text=piece,
                    page_number=block.page_number,
                    start_offset=block.start_offset + start,
                    end_offset=block.start_offset + end,
                    heading=block.heading,
                    heading_path=block.heading_path,
                )
            )

            start = end

        return pieces