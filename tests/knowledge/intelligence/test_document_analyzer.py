"""
Tests for DocumentAnalyzer.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from athena.domain.document import Document

from athena.knowledge.acquisition.domain.knowledge_representation import (
    KnowledgeRepresentation,
)

from athena.knowledge.intelligence.document_analyzer import (
    DocumentAnalyzer,
)


def create_document() -> Document:
    """Create test document."""

    now = datetime.now(
        timezone.utc,
    )

    return Document(
        id=uuid4(),
        filename="report.pdf",
        title="Test Report",
        file_path=Path(
            "/tmp/report.pdf",
        ),
        file_type="pdf",
        file_size=1024,
        created_at=now,
        updated_at=now,
    )


def test_document_analyzer_creates_profile() -> None:
    """Analyzer creates document profile."""

    analyzer = DocumentAnalyzer()

    document = create_document()

    representation = KnowledgeRepresentation(
        title="Test Report",
    )

    result = analyzer.analyze(
        document,
        representation,
    )

    assert (
        result.title
        == "Test Report"
    )

    assert (
        result.document_type
        == "pdf"
    )


def test_document_analyzer_counts_structure_nodes() -> None:
    """Analyzer includes representation structure."""

    analyzer = DocumentAnalyzer()

    document = create_document()

    representation = KnowledgeRepresentation(
        title="Test Report",
    )

    representation.add_node(
        uuid4(),
    )

    representation.add_node(
        uuid4(),
    )

    result = analyzer.analyze(
        document,
        representation,
    )

    assert (
        result.section_count
        == 2
    )

    assert (
        result.metadata["filename"]
        == "report.pdf"
    )