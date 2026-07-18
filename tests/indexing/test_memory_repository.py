"""
Tests for the in-memory chunk repository.
"""

from __future__ import annotations

from athena.indexing.models import DocumentChunk
from athena.indexing.repositories.memory import (
    MemoryChunkRepository,
)


def make_chunk(
    document_id: str,
    index: int,
) -> DocumentChunk:
    """Create a test chunk."""

    return DocumentChunk(
        chunk_id=f"{document_id}:{index}",
        document_id=document_id,
        chunk_index=index,
        page_number=1,
        text=f"Chunk {index}",
    )


def test_save_and_load_chunks() -> None:
    """Saved chunks can be loaded."""

    repository = MemoryChunkRepository()

    chunks = [
        make_chunk("doc-1", 0),
        make_chunk("doc-1", 1),
    ]

    repository.save_chunks(chunks)

    loaded = repository.load_chunks("doc-1")

    assert loaded == chunks


def test_load_unknown_document_returns_empty_list() -> None:
    """Unknown documents return an empty list."""

    repository = MemoryChunkRepository()

    assert repository.load_chunks("missing") == []


def test_delete_chunks() -> None:
    """Deleting a document removes its chunks."""

    repository = MemoryChunkRepository()

    repository.save_chunks(
        [
            make_chunk("doc-1", 0),
        ]
    )

    repository.delete_chunks("doc-1")

    assert repository.load_chunks("doc-1") == []


def test_delete_unknown_document() -> None:
    """Deleting an unknown document does not fail."""

    repository = MemoryChunkRepository()

    repository.delete_chunks("missing")

    assert repository.load_chunks("missing") == []


def test_replace_existing_chunks() -> None:
    """Saving new chunks replaces existing chunks."""

    repository = MemoryChunkRepository()

    repository.save_chunks(
        [
            make_chunk("doc-1", 0),
        ]
    )

    repository.save_chunks(
        [
            make_chunk("doc-1", 0),
            make_chunk("doc-1", 1),
            make_chunk("doc-1", 2),
        ]
    )

    loaded = repository.load_chunks("doc-1")

    assert len(loaded) == 3
    assert loaded[2].chunk_index == 2


def test_load_returns_copy() -> None:
    """Returned lists are defensive copies."""

    repository = MemoryChunkRepository()

    repository.save_chunks(
        [
            make_chunk("doc-1", 0),
        ]
    )

    loaded = repository.load_chunks("doc-1")

    loaded.clear()

    assert len(repository.load_chunks("doc-1")) == 1
