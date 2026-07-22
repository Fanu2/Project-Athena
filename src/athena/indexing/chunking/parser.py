"""
Document parser.

Converts extracted documents into ordered DocumentBlock objects.
"""

from __future__ import annotations

from athena.indexing.chunking.detectors import (
    CodeDetector,
    HeadingDetector,
    ListDetector,
    TableDetector,
)
from athena.indexing.chunking.models import (
    BlockType,
    DocumentBlock,
    ExtractedDocument,
)


class DocumentParser:
    """
    Converts extracted documents into logical document blocks.

    Responsibilities
    ----------------
    - Preserve reading order.
    - Split pages into paragraphs.
    - Detect structural block types.
    - Produce DocumentBlock objects.

    Does NOT:
    - Chunk text
    - Split oversized blocks
    - Generate metadata
    """

    def __init__(self) -> None:
        self._heading = HeadingDetector()
        self._list = ListDetector()
        self._table = TableDetector()
        self._code = CodeDetector()

    def parse(
        self,
        document: ExtractedDocument,
    ) -> list[DocumentBlock]:
        """
        Parse an extracted document into structural blocks.
        """

        blocks: list[DocumentBlock] = []

        heading_stack: list[str] = []

        for page in document.pages:
            offset = 0

            for paragraph in self._split_paragraphs(page.text):
                text = paragraph.strip()

                if not text:
                    offset += len(paragraph)
                    continue

                block_type = self._detect_type(text)

                heading = None

                if block_type is BlockType.HEADING:
                    heading = text
                    heading_stack.append(text)

                blocks.append(
                    DocumentBlock(
                        block_type=block_type,
                        text=text,
                        page_number=page.page_number,
                        start_offset=offset,
                        end_offset=offset + len(text),
                        heading=heading,
                        heading_path=tuple(heading_stack),
                    )
                )

                offset += len(paragraph)

        return blocks

    def _detect_type(
        self,
        text: str,
    ) -> BlockType:
        """
        Detect the logical type of a paragraph.
        """

        if self._heading.is_match(text):
            return BlockType.HEADING

        if self._list.is_match(text):
            return BlockType.LIST

        if self._table.is_match(text):
            return BlockType.TABLE

        if self._code.is_match(text):
            return BlockType.CODE

        return BlockType.PARAGRAPH

    @staticmethod
    def _split_paragraphs(
        text: str,
    ) -> list[str]:
        """
        Split page text into paragraphs.

        Initial implementation:
        blank line separation.

        Future versions may use
        PDF layout information,
        DOCX styles,
        Markdown,
        HTML,
        etc.
        """

        return [p for p in text.split("\n\n") if p.strip()]
