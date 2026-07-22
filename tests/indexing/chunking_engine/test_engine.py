"""
Tests for the structure-aware chunking engine.
"""

from __future__ import annotations

from athena.indexing.chunking_engine.engine import ChunkingEngine
from athena.indexing.models import DocumentChunk


def test_engine_returns_document_chunks(sample_document):
    """Engine should return a list of DocumentChunk objects."""

    engine = ChunkingEngine()

    chunks = engine.process(sample_document)

    assert isinstance(chunks, list)
    assert chunks
    assert all(isinstance(chunk, DocumentChunk) for chunk in chunks)


def test_engine_handles_empty_document(empty_document):
    """Engine should gracefully handle empty documents."""

    engine = ChunkingEngine()

    chunks = engine.process(empty_document)

    assert isinstance(chunks, list)


def test_engine_preserves_document_id(sample_document):
    """Every chunk should reference the source document."""

    engine = ChunkingEngine()

    chunks = engine.process(sample_document)

    assert all(
        chunk.document_id == sample_document.document_id
        for chunk in chunks
    )


def test_engine_chunk_indices_are_sequential(sample_document):
    """Chunk indices should be sequential."""

    engine = ChunkingEngine()

    chunks = engine.process(sample_document)

    for index, chunk in enumerate(chunks):
        assert chunk.chunk_index == index


def test_engine_chunk_text_not_empty(sample_document):
    """Generated chunks should contain text."""

    engine = ChunkingEngine()

    chunks = engine.process(sample_document)

    assert all(chunk.text.strip() for chunk in chunks)


def test_engine_offsets_are_valid(sample_document):
    """Chunk offsets should be valid."""

    engine = ChunkingEngine()

    chunks = engine.process(sample_document)

    for chunk in chunks:
        assert chunk.start_offset >= 0
        assert chunk.end_offset >= chunk.start_offset


def test_engine_page_numbers_valid(sample_document):
    """Chunk page numbers should be valid."""

    engine = ChunkingEngine()

    chunks = engine.process(sample_document)

    for chunk in chunks:
        assert chunk.page_number >= 1


def test_engine_handles_multi_page_document(
    multi_page_document,
):
    """Engine should process multi-page documents."""

    engine = ChunkingEngine()

    chunks = engine.process(
        multi_page_document,
    )

    assert chunks
    assert all(
        chunk.document_id == multi_page_document.document_id
        for chunk in chunks
    )


def test_engine_handles_long_document(
    long_document,
):
    """Large documents should be split into one or more chunks."""

    engine = ChunkingEngine()

    chunks = engine.process(
        long_document,
    )

    assert len(chunks) >= 1