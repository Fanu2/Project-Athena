"""
Unit tests for the ChunkBuilder.
"""

from __future__ import annotations

from athena.indexing.chunking_engine.builder import (
    ChunkBuilder,
)
from athena.indexing.chunking_engine.models import (
    ChunkType,
    DocumentBlock,
)
from athena.indexing.models import BlockType


def test_single_block_creates_single_chunk(
    sample_block: DocumentBlock,
):
    """One block should produce one chunk candidate."""

    builder = ChunkBuilder()

    result = builder.build(
        [sample_block],
    )

    assert len(result) == 1
    assert result[0].text == sample_block.text


def test_multiple_small_blocks_are_combined():
    """Small blocks should be combined into one chunk."""

    blocks = [
        DocumentBlock(
            block_type=BlockType.PARAGRAPH,
            text="First paragraph.",
            page_number=1,
            start_offset=0,
            end_offset=17,
        ),
        DocumentBlock(
            block_type=BlockType.PARAGRAPH,
            text="Second paragraph.",
            page_number=1,
            start_offset=19,
            end_offset=37,
        ),
    ]

    builder = ChunkBuilder(
        max_characters=100,
    )

    result = builder.build(
        blocks,
    )

    assert len(result) == 1
    assert "First paragraph." in result[0].text
    assert "Second paragraph." in result[0].text


def test_large_block_remains_single_candidate(
    long_document,
):
    """
    Builder should assemble blocks only.

    Splitting is handled by ChunkSplitter.
    """

    block = DocumentBlock(
        block_type=BlockType.PARAGRAPH,
        text=long_document.text,
        page_number=1,
        start_offset=0,
        end_offset=len(long_document.text),
    )

    builder = ChunkBuilder()

    result = builder.build(
        [block],
    )

    assert len(result) == 1
    assert result[0].text == long_document.text


def test_heading_information_is_preserved():
    """Heading metadata should be copied."""

    block = DocumentBlock(
        block_type=BlockType.HEADING,
        text="Introduction",
        page_number=1,
        start_offset=0,
        end_offset=12,
        heading="Introduction",
        heading_path=("Introduction",),
    )

    builder = ChunkBuilder()

    result = builder.build(
        [block],
    )

    assert result[0].heading == "Introduction"
    assert result[0].heading_path == (
        "Introduction",
    )


def test_mixed_blocks_create_mixed_chunk_type():
    """Different block types should create MIXED chunks."""

    blocks = [
        DocumentBlock(
            block_type=BlockType.HEADING,
            text="Heading",
            page_number=1,
            start_offset=0,
            end_offset=7,
        ),
        DocumentBlock(
            block_type=BlockType.PARAGRAPH,
            text="Paragraph",
            page_number=1,
            start_offset=9,
            end_offset=18,
        ),
    ]

    builder = ChunkBuilder()

    result = builder.build(
        blocks,
    )

    assert result[0].chunk_type == ChunkType.MIXED


def test_empty_input_returns_empty_list():
    """Empty input should produce no chunks."""

    builder = ChunkBuilder()

    result = builder.build([])

    assert result == []