"""
End-to-end tests for the indexing service.
"""

from __future__ import annotations

from pathlib import Path

from athena.indexing.repositories.memory import (
    MemoryChunkRepository,
)
from athena.indexing.service import (
    IndexingService,
)


def test_index_text_file(tmp_path: Path) -> None:
    """A text file can be indexed."""

    document = tmp_path / "sample.txt"

    document.write_text(
        "This is a simple test document.\n" * 100,
        encoding="utf-8",
    )

    repository = MemoryChunkRepository()

    service = IndexingService(repository)

    chunks = service.index_document(document)

    assert len(chunks) > 0

    stored = repository.load_chunks(
        chunks[0].document_id,
    )

    assert stored == chunks


def test_reindex_replaces_chunks(
    tmp_path: Path,
) -> None:
    """Reindexing replaces previous chunks."""

    document = tmp_path / "sample.txt"

    document.write_text(
        "Hello world " * 300,
        encoding="utf-8",
    )

    repository = MemoryChunkRepository()

    service = IndexingService(repository)

    first = service.index_document(document)

    document.write_text(
        "Completely different text " * 20,
        encoding="utf-8",
    )

    second = service.index_document(document)

    stored = repository.load_chunks(
        second[0].document_id,
    )

    assert stored == second

    assert stored != first
