"""
Unit tests for the document parser.
"""

from __future__ import annotations

from athena.indexing.chunking_engine.parser import DocumentParser
from athena.indexing.models import BlockType


def test_parser_returns_blocks(sample_document):
    """Parser should return a list of DocumentBlock objects."""

    parser = DocumentParser()

    blocks = parser.parse(sample_document)

    assert isinstance(blocks, list)
    assert blocks


def test_parser_preserves_page_numbers(sample_document):
    """Every parsed block should have a valid page number."""

    parser = DocumentParser()

    blocks = parser.parse(sample_document)

    assert all(block.page_number >= 1 for block in blocks)


def test_parser_detects_heading(sample_document):
    """Parser should identify heading blocks."""

    parser = DocumentParser()

    blocks = parser.parse(sample_document)

    assert any(
        block.block_type == BlockType.HEADING
        for block in blocks
    )


def test_parser_produces_paragraph_blocks(sample_document):
    """Parser should produce paragraph blocks."""

    parser = DocumentParser()

    blocks = parser.parse(sample_document)

    assert any(
        block.block_type == BlockType.PARAGRAPH
        for block in blocks
    )


def test_parser_offsets_are_valid(sample_document):
    """Offsets should always be valid."""

    parser = DocumentParser()

    blocks = parser.parse(sample_document)

    for block in blocks:
        assert block.start_offset >= 0
        assert block.end_offset >= block.start_offset


def test_parser_handles_empty_document(empty_document):
    """Parser should gracefully handle an empty document."""

    parser = DocumentParser()

    blocks = parser.parse(empty_document)

    assert isinstance(blocks, list)


def test_parser_handles_multi_page_document(
    multi_page_document,
):
    """Parser should process every page."""

    parser = DocumentParser()

    blocks = parser.parse(
        multi_page_document,
    )

    assert blocks

    pages = {block.page_number for block in blocks}

    assert pages == {1, 2}