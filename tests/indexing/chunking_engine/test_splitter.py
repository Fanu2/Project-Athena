"""
Unit tests for the structure-aware chunk splitter.
"""

from __future__ import annotations

from athena.indexing.chunking_engine.splitter import (
    ChunkSplitter,
)
from athena.indexing.chunking_engine.models import (
    DocumentBlock,
)
from athena.indexing.models import BlockType


def test_small_block_is_not_split(
    sample_block: DocumentBlock,
):
    """Small blocks should pass through unchanged."""

    splitter = ChunkSplitter(
        max_characters=100,
    )

    result = splitter.split(
        [sample_block],
    )

    assert len(result) == 1
    assert result[0].text == sample_block.text


def test_large_block_is_split(
    long_document,
):
    """Large blocks should be split."""

    block = DocumentBlock(
        block_type=BlockType.PARAGRAPH,
        text=long_document.text,
        page_number=1,
        start_offset=0,
        end_offset=len(long_document.text),
    )

    splitter = ChunkSplitter(
        max_characters=100,
    )

    result = splitter.split(
        [block],
    )

    assert len(result) > 1


def test_split_preserves_block_type(
    long_document,
):
    """Split blocks should preserve their type."""

    block = DocumentBlock(
        block_type=BlockType.PARAGRAPH,
        text=long_document.text,
        page_number=1,
        start_offset=0,
        end_offset=len(long_document.text),
    )

    splitter = ChunkSplitter(
        max_characters=100,
    )

    result = splitter.split(
        [block],
    )

    assert all(
        item.block_type == BlockType.PARAGRAPH
        for item in result
    )


def test_split_preserves_page_number(
    long_document,
):
    """Split blocks should preserve page numbers."""

    block = DocumentBlock(
        block_type=BlockType.PARAGRAPH,
        text=long_document.text,
        page_number=3,
        start_offset=0,
        end_offset=len(long_document.text),
    )

    splitter = ChunkSplitter(
        max_characters=100,
    )

    result = splitter.split(
        [block],
    )

    assert all(
        item.page_number == 3
        for item in result
    )


def test_split_offsets_are_valid(
    long_document,
):
    """Split offsets should remain valid."""

    block = DocumentBlock(
        block_type=BlockType.PARAGRAPH,
        text=long_document.text,
        page_number=1,
        start_offset=0,
        end_offset=len(long_document.text),
    )

    splitter = ChunkSplitter(
        max_characters=100,
    )

    result = splitter.split(
        [block],
    )

    for item in result:
        assert item.start_offset >= block.start_offset
        assert item.end_offset <= block.end_offset
        assert item.end_offset >= item.start_offset


def test_empty_input_returns_empty_list():
    """Empty input should produce no blocks."""

    splitter = ChunkSplitter()

    result = splitter.split([])

    assert result == []