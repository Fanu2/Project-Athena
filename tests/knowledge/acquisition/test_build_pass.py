"""
Tests for Athena Build Pass.
"""

from unittest.mock import Mock

from athena.knowledge.acquisition.pipeline.build_pass import (
    BuildPass,
)

from athena.knowledge.acquisition.domain.knowledge_candidate import (
    KnowledgeCandidate,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)


def test_build_pass_creates_knowledge_object() -> None:
    """
    Build pass creates canonical knowledge object.
    """

    candidate = KnowledgeCandidate(
        candidate_type="document",
        value="Athena",
        confidence=0.8,
    )

    result = BuildPass().execute(
        KnowledgeContext(),
        [candidate],
    )

    assert len(result) == 1

    obj = result[0]

    assert obj.object_type == "document"

    assert obj.title == "Athena"

    assert obj.confidence == 0.8


def test_build_pass_creates_evidence_and_citation() -> None:
    """
    Build pass creates evidence and citation
    from knowledge objects.
    """

    context = KnowledgeContext()

    evidence_builder = Mock()

    citation_builder = Mock()

    evidence = Mock()

    evidence_builder.build.return_value = (
        evidence
    )

    context.add_service(
        "evidence_build_service",
        evidence_builder,
    )

    context.add_service(
        "citation_build_service",
        citation_builder,
    )

    candidate = KnowledgeCandidate(
        candidate_type="document",
        value="Athena",
        confidence=0.8,
    )

    result = BuildPass().execute(
        context,
        [candidate],
    )

    assert len(result) == 1

    evidence_builder.build.assert_called_once()

    citation_builder.build.assert_called_once_with(
        evidence,
    )