"""
Unit tests for MetadataBuilder.
"""

from __future__ import annotations

from athena.indexing.chunking_engine.metadata import (
    MetadataBuilder,
)
from athena.indexing.models import ChunkType


def test_build_creates_document_chunks(
    sample_document,
    sample_candidate,
):
    """Metadata builder should create DocumentChunk objects."""

    builder = MetadataBuilder()

    result = builder.build(
        sample_document,
        [sample_candidate],
    )

    assert len(result) == 1

    chunk = result[0]

    assert chunk.document_id == sample_document.document_id
    assert chunk.text == sample_candidate.text


def test_chunk_ids_are_generated(
    sample_document,
    sample_candidate,
):
    """Each chunk should receive a unique ID."""

    builder = MetadataBuilder()

    result = builder.build(
        sample_document,
        [sample_candidate],
    )

    assert result[0].chunk_id


def test_chunk_indexes_are_sequential(
    sample_document,
    sample_candidate,
):
    """Chunk indexes should start at zero."""

    builder = MetadataBuilder()

    result = builder.build(
        sample_document,
        [
            sample_candidate,
            sample_candidate,
        ],
    )

    assert result[0].chunk_index == 0
    assert result[1].chunk_index == 1


def test_page_number_is_preserved(
    sample_document,
    sample_candidate,
):
    """Page information should be copied."""

    builder = MetadataBuilder()

    result = builder.build(
        sample_document,
        [sample_candidate],
    )

    assert result[0].page_number == sample_candidate.page_number


def test_offsets_are_preserved(
    sample_document,
    sample_candidate,
):
    """Offsets should come from source blocks."""

    builder = MetadataBuilder()

    result = builder.build(
        sample_document,
        [sample_candidate],
    )

    chunk = result[0]

    assert chunk.start_offset == (
        sample_candidate.blocks[0].start_offset
    )

    assert chunk.end_offset == (
        sample_candidate.blocks[-1].end_offset
    )


def test_heading_metadata_is_preserved(
    sample_document,
    heading_block,
):
    """Heading information should survive conversion."""

    from athena.indexing.models import ChunkCandidate

    candidate = ChunkCandidate(
        blocks=[heading_block],
        text=heading_block.text,
        page_number=heading_block.page_number,
        heading=heading_block.heading,
        heading_path=heading_block.heading_path,
        chunk_type=ChunkType.HEADING,
    )

    builder = MetadataBuilder()

    result = builder.build(
        sample_document,
        [candidate],
    )

    chunk = result[0]

    assert chunk.heading == heading_block.heading
    assert chunk.heading_path == heading_block.heading_path


def test_chunk_type_is_preserved(
    sample_document,
    sample_candidate,
):
    """Chunk classification should be preserved."""

    builder = MetadataBuilder()

    result = builder.build(
        sample_document,
        [sample_candidate],
    )

    assert result[0].chunk_type == (
        sample_candidate.chunk_type
    )


def test_empty_candidates_returns_empty_list(
    sample_document,
):
    """No candidates should produce no chunks."""

    builder = MetadataBuilder()

    result = builder.build(
        sample_document,
        [],
    )

    assert result == []