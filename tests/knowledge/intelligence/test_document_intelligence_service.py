"""
Tests for DocumentIntelligenceService.
"""

from __future__ import annotations

from athena.knowledge.intelligence.document_intelligence_service import (
    DocumentIntelligenceService,
)

from athena.knowledge.intelligence.document_analyzer import (
    DocumentAnalyzer,
)


def test_service_uses_default_analyzer() -> None:
    """Service creates analyzer by default."""

    service = DocumentIntelligenceService()

    assert isinstance(
        service._analyzer,
        DocumentAnalyzer,
    )


def test_service_accepts_custom_analyzer() -> None:
    """Service accepts injected analyzer."""

    analyzer = DocumentAnalyzer()

    service = DocumentIntelligenceService(
        analyzer=analyzer,
    )

    assert (
        service._analyzer
        is analyzer
    )