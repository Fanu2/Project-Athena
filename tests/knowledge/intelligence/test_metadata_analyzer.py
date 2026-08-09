"""
Tests for MetadataAnalyzer.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from athena.domain.document import Document

from athena.knowledge.intelligence import (
    MetadataAnalyzer,
)


def create_document() -> Document:
    """Create test document."""

    now = datetime.now(
        timezone.utc,
    )

    return Document(
        id=uuid4(),
        filename="research.pdf",
        title="Research Paper",
        file_path=Path(
            "/tmp/research.pdf",
        ),
        file_type="pdf",
        file_size=4096,
        created_at=now,
        updated_at=now,
    )


def test_metadata_analyzer_extracts_document_type() -> None:
    """Analyzer extracts document type."""

    analyzer = MetadataAnalyzer()

    result = analyzer.analyze(
        create_document(),
    )

    assert (
        result.document_type
        == "pdf"
    )


def test_metadata_analyzer_preserves_source_metadata() -> None:
    """Analyzer preserves document metadata."""

    analyzer = MetadataAnalyzer()

    result = analyzer.analyze(
        create_document(),
    )

    assert (
        result.metadata["filename"]
        == "research.pdf"
    )

    assert (
        result.metadata["file_size"]
        == 4096
    )


def test_metadata_confidence_is_valid() -> None:
    """Metadata confidence is initialized."""

    analyzer = MetadataAnalyzer()

    result = analyzer.analyze(
        create_document(),
    )

    assert (
        result.confidence
        == 1.0
    )