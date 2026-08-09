"""
Tests for Athena Document Intelligence Pass.
"""

from __future__ import annotations

from unittest.mock import Mock

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)

from athena.knowledge.acquisition.domain.knowledge_representation import (
    KnowledgeRepresentation,
)

from athena.knowledge.acquisition.pipeline.intelligence_pass import (
    IntelligencePass,
)


def test_intelligence_pass_stores_result() -> None:
    """
    Intelligence result is stored in runtime context.
    """

    service = Mock()

    intelligence = Mock()

    service.analyze.return_value = intelligence

    document = Mock()

    context = KnowledgeContext()

    context.add_service(
        "document",
        document,
    )

    representation = KnowledgeRepresentation(
        title="Athena Document",
    )

    stage = IntelligencePass(
        service=service,
    )

    result = stage.execute(
        context,
        representation,
    )

    assert result is representation

    assert (
        context.get_service(
            "document_intelligence",
        )
        is intelligence
    )

    service.analyze.assert_called_once_with(
        document,
        representation,
    )


def test_intelligence_pass_builds_document_evidence() -> None:
    """
    Intelligence pass triggers evidence persistence.
    """

    service = Mock()

    intelligence = Mock()

    service.analyze.return_value = intelligence

    evidence_service = Mock()

    document = Mock()

    context = KnowledgeContext()

    context.add_service(
        "document",
        document,
    )

    context.add_service(
        "document_evidence_service",
        evidence_service,
    )

    representation = KnowledgeRepresentation(
        title="Athena Document",
    )

    stage = IntelligencePass(
        service=service,
    )

    result = stage.execute(
        context,
        representation,
    )

    assert result is representation

    assert (
        context.get_service(
            "document_intelligence",
        )
        is intelligence
    )

    evidence_service.build.assert_called_once_with(
        document,
    )


def test_intelligence_pass_skips_unknown_input() -> None:
    """
    Non representation input passes unchanged.
    """

    context = KnowledgeContext()

    stage = IntelligencePass()

    value = "test"

    result = stage.execute(
        context,
        value,
    )

    assert result == value