"""
Tests for the SQLite chunk repository.
"""

from __future__ import annotations

import uuid

from athena.indexing.models import DocumentChunk
from athena.indexing.repositories.sqlite import (
    SQLiteChunkRepository,
)


def make_chunk(
    index: int,
) -> DocumentChunk:
    """Create a test chunk."""

    return DocumentChunk(
        chunk_id=str(uuid.uuid4()),
        document_id="document-1",
        chunk_index=index,
        page_number=1,
        text=f"Chunk {index}",
    )


def test_save_and_load_chunks(
    tmp_path,
) -> None:
    """Chunks can be saved and loaded."""

    database = tmp_path / "chunks.db"

    repository = SQLiteChunkRepository(
        database,
    )

    chunks = [
        make_chunk(0),
        make_chunk(1),
        make_chunk(2),
    ]

    repository.save_chunks(chunks)

    loaded = repository.load_chunks(
        "document-1",
    )

    assert len(loaded) == 3
    assert loaded[0].text == "Chunk 0"
    assert loaded[1].text == "Chunk 1"
    assert loaded[2].text == "Chunk 2"


def test_delete_chunks(
    tmp_path,
) -> None:
    """Chunks can be deleted."""

    database = tmp_path / "chunks.db"

    repository = SQLiteChunkRepository(
        database,
    )

    repository.save_chunks(
        [
            make_chunk(0),
            make_chunk(1),
        ]
    )

    repository.delete_chunks(
        "document-1",
    )

    assert (
        repository.load_chunks(
            "document-1",
        )
        == []
    )


def test_repository_persists_data(
    tmp_path,
) -> None:
    """Chunks survive repository recreation."""

    database = tmp_path / "chunks.db"

    repository = SQLiteChunkRepository(
        database,
    )

    repository.save_chunks(
        [
            make_chunk(0),
            make_chunk(1),
        ]
    )

    repository = SQLiteChunkRepository(
        database,
    )

    loaded = repository.load_chunks(
        "document-1",
    )

    assert len(loaded) == 2
    assert loaded[0].chunk_index == 0
    assert loaded[1].chunk_index == 1


def test_save_replaces_existing_chunks(
    tmp_path,
) -> None:
    """Saving again replaces previous chunks."""

    database = tmp_path / "chunks.db"

    repository = SQLiteChunkRepository(
        database,
    )

    repository.save_chunks(
        [
            make_chunk(0),
            make_chunk(1),
        ]
    )

    repository.save_chunks(
        [
            make_chunk(5),
        ]
    )

    loaded = repository.load_chunks(
        "document-1",
    )

    assert len(loaded) == 1
    assert loaded[0].chunk_index == 5
