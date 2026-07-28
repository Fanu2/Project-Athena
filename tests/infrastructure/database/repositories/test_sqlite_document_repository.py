"""
Tests for SqliteDocumentRepository.
"""

from datetime import datetime
from pathlib import Path
from uuid import uuid4

from athena.domain import Document
from athena.infrastructure.database.repositories.sqlite_document_repository import (
    SqliteDocumentRepository,
)


def test_add_and_get_document(test_session):
    """Documents can be added and retrieved."""

    repository = SqliteDocumentRepository(test_session)

    document_id = uuid4()

    document = Document(
        id=document_id,
        filename="example.pdf",
        title="Example",
        file_path=Path("C:/docs/example.pdf"),
        file_type="pdf",
        file_size=1234,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    repository.add(document)

    loaded = repository.get(document_id)

    assert loaded is not None
    assert loaded.id == document_id
    assert loaded.filename == "example.pdf"
    assert loaded.title == "Example"
    assert loaded.file_type == "pdf"
    assert loaded.file_size == 1234


def test_get_returns_none_for_missing_document(test_session):
    """Unknown document returns None."""

    repository = SqliteDocumentRepository(test_session)

    assert repository.get(uuid4()) is None


def test_exists_by_path(test_session):
    """Repository can detect an existing document by path."""

    repository = SqliteDocumentRepository(test_session)

    document = Document(
        id=uuid4(),
        filename="example.pdf",
        title="Example",
        file_path=Path("C:/docs/example.pdf"),
        file_type="pdf",
        file_size=1234,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    repository.add(document)

    assert repository.exists(str(document.file_path)) is True
    assert repository.exists(str(Path("C:/docs/missing.pdf"))) is False


def test_get_by_path(test_session):
    """Document can be retrieved by path."""

    repository = SqliteDocumentRepository(test_session)

    document = Document(
        id=uuid4(),
        filename="example.pdf",
        title="Example",
        file_path=Path("C:/docs/example.pdf"),
        file_type="pdf",
        file_size=1234,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    repository.add(document)

    loaded = repository.get_by_path(str(document.file_path))

    assert loaded is not None
    assert loaded.id == document.id
    assert loaded.filename == "example.pdf"

    assert repository.get_by_path(str(Path("C:/docs/missing.pdf"))) is None


def test_update_document(test_session):
    """Document can be updated."""

    repository = SqliteDocumentRepository(test_session)

    document = Document(
        id=uuid4(),
        filename="example.pdf",
        title="Original",
        file_path=Path("C:/docs/example.pdf"),
        file_type="pdf",
        file_size=1234,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    repository.add(document)

    updated = Document(
        id=document.id,
        filename="updated.pdf",
        title="Updated",
        file_path=Path("C:/docs/updated.pdf"),
        file_type="pdf",
        file_size=4321,
        created_at=document.created_at,
        updated_at=datetime.now(),
    )

    repository.update(updated)

    loaded = repository.get(document.id)

    assert loaded is not None
    assert loaded.filename == "updated.pdf"
    assert loaded.title == "Updated"
    assert loaded.file_path == Path("C:/docs/updated.pdf")
    assert loaded.file_size == 4321


def test_delete_document(test_session):
    """Document can be deleted."""

    repository = SqliteDocumentRepository(test_session)

    document = Document(
        id=uuid4(),
        filename="example.pdf",
        title="Example",
        file_path=Path("C:/docs/example.pdf"),
        file_type="pdf",
        file_size=1234,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    repository.add(document)

    assert repository.get(document.id) is not None

    repository.delete(document.id)

    assert repository.get(document.id) is None


def test_get_all_documents(test_session):
    """All documents can be retrieved."""

    repository = SqliteDocumentRepository(test_session)

    repository.add(
        Document(
            id=uuid4(),
            filename="alpha.pdf",
            title="Alpha",
            file_path=Path("C:/docs/alpha.pdf"),
            file_type="pdf",
            file_size=100,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
    )

    repository.add(
        Document(
            id=uuid4(),
            filename="beta.pdf",
            title="Beta",
            file_path=Path("C:/docs/beta.pdf"),
            file_type="pdf",
            file_size=200,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
    )

    documents = repository.get_all()

    assert len(documents) == 2

    filenames = {document.filename for document in documents}

    assert filenames == {"alpha.pdf", "beta.pdf"}

