"""
Tests for SqliteMetadataRepository.
"""

from uuid import uuid4

from athena.domain.document_metadata import DocumentMetadata
from athena.infrastructure.database.repositories.sqlite_metadata_repository import (
    SqliteMetadataRepository,
)


def test_document_metadata_defaults() -> None:
    metadata = DocumentMetadata(document_id=uuid4())

    assert metadata.language is None
    assert metadata.page_count is None
    assert metadata.metadata_version == 1


def test_document_metadata_values() -> None:
    document_id = uuid4()

    metadata = DocumentMetadata(
        document_id=document_id,
        language="en",
        page_count=25,
        metadata_version=2,
    )

    assert metadata.document_id == document_id
    assert metadata.language == "en"
    assert metadata.page_count == 25
    assert metadata.metadata_version == 2


def test_add_and_get_metadata(test_session):
    """Metadata can be added and retrieved."""

    repository = SqliteMetadataRepository(test_session)

    document_id = uuid4()

    metadata = DocumentMetadata(
        document_id=document_id,
        language="en",
        page_count=12,
    )

    repository.add(metadata)

    loaded = repository.get(document_id)

    assert loaded is not None
    assert loaded.document_id == document_id
    assert loaded.language == "en"
    assert loaded.page_count == 12


def test_get_returns_none_for_missing_metadata(test_session):
    """Unknown document metadata returns None."""

    repository = SqliteMetadataRepository(test_session)

    assert repository.get(uuid4()) is None

def test_update_metadata(test_session):
    """Metadata can be updated."""

    repository = SqliteMetadataRepository(test_session)

    document_id = uuid4()

    repository.add(
        DocumentMetadata(
            document_id=document_id,
            language="en",
            page_count=10,
        )
    )

    repository.update(
        DocumentMetadata(
            document_id=document_id,
            language="fr",
            page_count=20,
            metadata_version=2,
        )
    )

    loaded = repository.get(document_id)

    assert loaded is not None
    assert loaded.language == "fr"
    assert loaded.page_count == 20
    assert loaded.metadata_version == 2

def test_delete_metadata(test_session):
    """Metadata can be deleted."""

    repository = SqliteMetadataRepository(test_session)

    document_id = uuid4()

    repository.add(
        DocumentMetadata(
            document_id=document_id,
            language="en",
            page_count=15,
        )
    )

    assert repository.get(document_id) is not None

    repository.delete(document_id)

    assert repository.get(document_id) is None

def test_get_all_metadata(test_session):
    """All metadata records can be retrieved."""

    repository = SqliteMetadataRepository(test_session)

    repository.add(
        DocumentMetadata(
            document_id=uuid4(),
            language="en",
            page_count=10,
        )
    )

    repository.add(
        DocumentMetadata(
            document_id=uuid4(),
            language="fr",
            page_count=20,
        )
    )

    metadata = repository.get_all()

    assert len(metadata) == 2

    languages = {item.language for item in metadata}

    assert languages == {"en", "fr"}
