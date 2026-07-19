from datetime import datetime
from pathlib import Path

from athena.indexing.models import IndexedDocument
from athena.indexing.repositories.sqlite_document import (
    SQLiteDocumentRepository,
)


def test_exists_by_hash(tmp_path):
    database = tmp_path / "athena.db"

    repository = SQLiteDocumentRepository(database)

    document = IndexedDocument(
        document_id="doc1",
        path=Path("sample.pdf"),
        title="Sample",
        sha256="abc123",
        page_count=5,
        indexed_at=datetime.now(),
    )

    repository.save_document(document)

    assert repository.exists_by_hash("abc123")
    assert not repository.exists_by_hash("xyz789")


def test_load_document(tmp_path):
    database = tmp_path / "athena.db"

    repository = SQLiteDocumentRepository(database)

    document = IndexedDocument(
        document_id="doc1",
        path=Path("sample.pdf"),
        title="Sample",
        sha256="abc123",
        page_count=5,
        indexed_at=datetime.now(),
    )

    repository.save_document(document)

    loaded = repository.load_document("doc1")

    assert loaded is not None
    assert loaded.document_id == "doc1"
    assert loaded.sha256 == "abc123"
    assert loaded.title == "Sample"
