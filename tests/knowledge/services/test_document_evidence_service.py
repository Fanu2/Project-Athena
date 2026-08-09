"""
Tests for Athena Document Evidence Service.
"""

from __future__ import annotations

from unittest.mock import Mock

from athena.knowledge.services.document_evidence_service import (
    DocumentEvidenceService,
)


def test_document_evidence_service_builds_evidence_records() -> None:
    """
    Document evidence service converts
    profiles into persistent records.
    """

    analyzer = Mock()

    adapter = Mock()

    builder = Mock()

    profile = Mock()

    record = Mock()

    analyzer.analyze.return_value = [
        profile,
    ]

    adapter.to_record.return_value = (
        record
    )

    service = DocumentEvidenceService(
        builder=builder,
        analyzer=analyzer,
        adapter=adapter,
    )

    document = Mock()

    result = service.build(
        document,
    )

    assert result == [
        record,
    ]

    analyzer.analyze.assert_called_once_with(
        document,
    )

    adapter.to_record.assert_called_once_with(
        profile,
    )

    builder.build_record.assert_called_once_with(
        record,
    )