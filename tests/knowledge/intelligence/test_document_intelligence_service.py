"""
Tests for DocumentIntelligenceService.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from athena.domain.document import Document

from athena.knowledge.acquisition.domain.knowledge_representation import (
    KnowledgeRepresentation,
)

from athena.knowledge.intelligence import (
    DocumentIntelligenceService,
)


def create_document() -> Document:
    """Create test document."""

    now = datetime.now(
        timezone.utc,
    )

    return Document(
        id=uuid4(),
        filename="athena.pdf",
        title="Athena Document",
        file_path=Path(
            "/tmp/athena.pdf",
        ),
        file_type="pdf",
        file_size=2048,
        created_at=now,
        updated_at=now,
    )


def test_service_generates_complete_intelligence() -> None:
    """Service combines all intelligence layers."""

    service = DocumentIntelligenceService()

    document = create_document()

    representation = KnowledgeRepresentation(
        title="Athena Document",
    )

    representation.add_node(
        uuid4(),
    )

    result = service.analyze(
        document,
        representation,
    )

    assert (
        result.profile.title
        == "Athena Document"
    )

    assert (
        result.metadata.document_type
        == "pdf"
    )

    assert (
        len(result.structure)
        == 1
    )


def test_service_preserves_document_metadata() -> None:
    """Service keeps source metadata."""

    service = DocumentIntelligenceService()

    result = service.analyze(
        create_document(),
        KnowledgeRepresentation(
            title="Athena Document",
        ),
    )

    assert (
        result.metadata.metadata["filename"]
        == "athena.pdf"
    )

    assert (
        result.profile.metadata["file_size"]
        == 2048
    )