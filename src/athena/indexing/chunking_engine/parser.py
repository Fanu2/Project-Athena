"""
Structure-aware document parser.

The parser converts an ExtractedDocument into an ordered sequence of
DocumentBlock objects while preserving document structure.

Responsibilities
----------------
* Split extracted text into logical paragraphs.
* Detect the structural type of each paragraph.
* Preserve reading order.
* Track page numbers and character offsets.

The parser deliberately does NOT perform chunking. Chunk construction
is handled later by ChunkBuilder.
"""

from __future__ import annotations

from collections.abc import Sequence

from athena.indexing.chunking_engine.detectors import (
    DEFAULT_DETECTORS,
    BaseDetector,
)
from athena.indexing.chunking_engine.models import (
    BlockType,
    DocumentBlock,
)
from athena.indexing.models import ExtractedDocument


class DocumentParser:
    """
    Converts an ExtractedDocument into DocumentBlocks.
    """

    def __init__(
        self,
        detectors: Sequence[BaseDetector] = DEFAULT_DETECTORS,
    ) -> None:
        self._detectors = tuple(detectors)

    def parse(
        self,
        document: ExtractedDocument,
    ) -> list[DocumentBlock]:
        """
        Parse an extracted document into structural blocks.
        """

        blocks: list[DocumentBlock] = []

        offset = 0

        for paragraph in self._split_paragraphs(document.text):

            block_type = self._detect_block_type(paragraph)

            start = document.text.find(paragraph, offset)

            end = start + len(paragraph)

            blocks.append(
                DocumentBlock(
                    block_type=block_type,
                    text=paragraph,
                    page_number=1,
                    start_offset=start,
                    end_offset=end,
                )
            )

            offset = end

        return blocks

    @staticmethod
    def _split_paragraphs(text: str) -> list[str]:
        """
        Split text into logical paragraphs.

        Empty paragraphs are discarded.
        """

        return [
            paragraph.strip()
            for paragraph in text.split("\n\n")
            if paragraph.strip()
        ]

    def _detect_block_type(
        self,
        text: str,
    ) -> BlockType:
        """
        Determine the logical type of a paragraph.
        """

        for detector in self._detectors:
            if detector.is_match(text):
                return detector.block_type

        return BlockType.PARAGRAPH