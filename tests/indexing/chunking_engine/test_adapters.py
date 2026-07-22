"""
Tests for chunking adapter integration.
"""

from __future__ import annotations

from athena.indexing.chunking_engine.legacy_adapter import (
    LegacyChunkingAdapter,
)

from athena.indexing.chunking_engine.structure_adapter import (
    StructureChunkingAdapter,
)

from athena.indexing.models import DocumentChunk


def test_legacy_adapter_returns_chunks(
    sample_document,
):
    """Legacy adapter should return document chunks."""

    adapter = LegacyChunkingAdapter()

    chunks = adapter.chunk_document(
        sample_document,
    )

    assert isinstance(chunks, list)

    assert all(
        isinstance(chunk, DocumentChunk)
        for chunk in chunks
    )


def test_structure_adapter_returns_chunks(
    sample_document,
):
    """Structure adapter should return document chunks."""

    adapter = StructureChunkingAdapter()

    chunks = adapter.chunk_document(
        sample_document,
    )

    assert isinstance(chunks, list)

    assert all(
        isinstance(chunk, DocumentChunk)
        for chunk in chunks
    )


def test_both_adapters_preserve_document_id(
    sample_document,
):
    """Both adapters should preserve source document ID."""

    adapters = [
        LegacyChunkingAdapter(),
        StructureChunkingAdapter(),
    ]

    for adapter in adapters:
        chunks = adapter.chunk_document(
            sample_document,
        )

        assert all(
            chunk.document_id
            == sample_document.document_id
            for chunk in chunks
        )