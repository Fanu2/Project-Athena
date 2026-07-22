"""
Structural detectors for the Athena Chunking Engine.

Each detector has a single responsibility:
identify one specific type of document structure.
"""

from __future__ import annotations

import re


class BaseDetector:
    """Base class for all detectors."""

    def is_match(self, text: str) -> bool:
        raise NotImplementedError


class HeadingDetector(BaseDetector):
    """Detect document headings."""

    _markdown = re.compile(r"^#{1,6}\s+.+$")
    _numbered = re.compile(r"^\d+(\.\d+)*\s+.+$")

    def is_match(self, text: str) -> bool:
        text = text.strip()

        if not text:
            return False

        if self._markdown.match(text):
            return True

        if self._numbered.match(text):
            return True

        words = text.split()

        if len(words) <= 12 and text == text.title() and not text.endswith("."):
            return True

        return False


class ListDetector(BaseDetector):
    """Detect bulleted and numbered lists."""

    _bullet = re.compile(r"^[-*•]\s+.+$")
    _number = re.compile(r"^\d+\.\s+.+$")

    def is_match(self, text: str) -> bool:
        text = text.strip()

        return bool(self._bullet.match(text) or self._number.match(text))


class TableDetector(BaseDetector):
    """Detect plain-text tables."""

    def is_match(self, text: str) -> bool:

        lines = [line.strip() for line in text.splitlines() if line.strip()]

        if len(lines) < 2:
            return False

        pipe_rows = sum("|" in line for line in lines)
        tab_rows = sum("\t" in line for line in lines)

        return pipe_rows >= 2 or tab_rows >= 2


class CodeDetector(BaseDetector):
    """Detect source code."""

    _keywords = (
        "def ",
        "class ",
        "import ",
        "from ",
        "return ",
        "if ",
        "for ",
        "while ",
    )

    def is_match(self, text: str) -> bool:

        text = text.strip()

        if text.startswith("```"):
            return True

        return any(keyword in text for keyword in self._keywords)
