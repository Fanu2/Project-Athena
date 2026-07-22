"""
Unit tests for document structure detectors.
"""

from __future__ import annotations

from athena.indexing.chunking_engine.detectors import (
    DEFAULT_DETECTORS,
)
from athena.indexing.models import BlockType


def detect(text: str):
    """
    Run the default detector chain.
    """

    for detector in DEFAULT_DETECTORS:
        if detector.is_match(text):
            return detector.block_type

    return BlockType.PARAGRAPH


def test_heading_detection():
    """Markdown headings should be detected."""

    result = detect(
        "# Introduction",
    )

    assert result == BlockType.HEADING


def test_second_level_heading_detection():
    """Sub-headings should be detected."""

    result = detect(
        "## Background",
    )

    assert result == BlockType.HEADING


def test_list_detection():
    """Bullet lists should be detected."""

    result = detect(
        "- First item\n- Second item",
    )

    assert result == BlockType.LIST


def test_numbered_list_detection():
    """Numbered lists should be detected."""

    result = detect(
        "1. First item\n2. Second item",
    )

    assert result == BlockType.LIST


def test_code_detection():
    """Code blocks should be detected."""

    result = detect(
        "```python\nprint('hello')\n```",
    )

    assert result == BlockType.CODE


def test_table_detection():
    """Markdown tables should be detected."""

    result = detect(
        "| Name | Value |\n"
        "| --- | --- |\n"
        "| A | 1 |",
    )

    assert result == BlockType.TABLE


def test_normal_text_is_paragraph():
    """Ordinary text should fallback to paragraph."""

    result = detect(
        "Athena is a local research assistant.",
    )

    assert result == BlockType.PARAGRAPH


def test_empty_text_is_paragraph():
    """Empty text should safely fallback."""

    result = detect("")

    assert result == BlockType.PARAGRAPH