"""
Structure detectors for the Athena Chunking Engine.

Each detector class is responsible for recognizing a single logical
document structure. The parser applies these detectors in order to
classify each document block.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod

from athena.indexing.chunking_engine.models import BlockType


class BaseDetector(ABC):
    """Base class for all structure detectors."""

    block_type: BlockType

    @abstractmethod
    def is_match(self, text: str) -> bool:
        """Return True if the text matches this detector."""
        raise NotImplementedError


class HeadingDetector(BaseDetector):
    """Detect headings."""

    block_type = BlockType.HEADING

    _patterns = (
        re.compile(r"^#{1,6}\s+"),                  # Markdown
        re.compile(r"^\d+(\.\d+)*\s+"),             # 1  1.1  2.3.4
        re.compile(r"^[A-Z][A-Z0-9\s\-]{2,}$"),     # ALL CAPS
    )

    def is_match(self, text: str) -> bool:
        text = text.strip()

        if not text:
            return False

        if len(text) > 120:
            return False

        return any(pattern.match(text) for pattern in self._patterns)


class ListDetector(BaseDetector):
    """Detect bullet and numbered lists."""

    block_type = BlockType.LIST

    _pattern = re.compile(
        r"^\s*(?:[-*•]|\d+[.)]|[a-zA-Z][.)])\s+"
    )

    def is_match(self, text: str) -> bool:
        return bool(self._pattern.match(text))


class TableDetector(BaseDetector):
    """Detect simple tables."""

    block_type = BlockType.TABLE

    def is_match(self, text: str) -> bool:
        text = text.strip()

        if "|" in text:
            return True

        if "\t" in text:
            return True

        return False


class CodeDetector(BaseDetector):
    """Detect code blocks."""

    block_type = BlockType.CODE

    _keywords = (
        "def ",
        "class ",
        "import ",
        "from ",
        "if ",
        "for ",
        "while ",
        "return ",
        "{",
        "};",
    )

    def is_match(self, text: str) -> bool:
        text = text.strip()

        if text.startswith("```"):
            return True

        return any(keyword in text for keyword in self._keywords)


DEFAULT_DETECTORS: tuple[BaseDetector, ...] = (
    HeadingDetector(),
    ListDetector(),
    TableDetector(),
    CodeDetector(),
)