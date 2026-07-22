"""
Sentence-aware block splitter.
"""

from __future__ import annotations

import re

from athena.indexing.chunking.models import DocumentBlock


class ChunkSplitter:
    """
    Splits oversized DocumentBlocks into smaller blocks.

    Splitting is sentence-aware whenever possible.
    """

    def __init__(
        self,
        max_chars: int = 1000,
        overlap: int = 100,
    ) -> None:
        self._max_chars = max_chars
        self._overlap = overlap

    def split(
        self,
        block: DocumentBlock,
    ) -> list[DocumentBlock]:
        """
        Split a DocumentBlock if necessary.
        """

        if len(block.text) <= self._max_chars:
            return [block]

        return self._split_sentences(block)

    def _split_sentences(
        self,
        block: DocumentBlock,
    ) -> list[DocumentBlock]:
        """
        Sentence-aware splitting.
        """

        sentences = re.split(
            r"(?<=[.!?])\s+",
            block.text,
        )

        blocks: list[DocumentBlock] = []

        current: list[str] = []

        start = block.start_offset

        offset = block.start_offset

        for sentence in sentences:
            tentative = " ".join(current + [sentence])

            if current and len(tentative) > self._max_chars:
                text = " ".join(current)

                blocks.append(
                    DocumentBlock(
                        block_type=block.block_type,
                        text=text,
                        page_number=block.page_number,
                        start_offset=start,
                        end_offset=start + len(text),
                        heading=block.heading,
                        heading_path=block.heading_path,
                    )
                )

                overlap_text = text[-self._overlap :]

                current = [overlap_text, sentence]

                start = offset - len(overlap_text)

            else:
                current.append(sentence)

            offset += len(sentence) + 1

        if current:
            text = " ".join(current)

            blocks.append(
                DocumentBlock(
                    block_type=block.block_type,
                    text=text,
                    page_number=block.page_number,
                    start_offset=start,
                    end_offset=start + len(text),
                    heading=block.heading,
                    heading_path=block.heading_path,
                )
            )

        return blocks
