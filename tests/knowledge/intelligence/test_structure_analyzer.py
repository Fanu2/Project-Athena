"""
Tests for StructureAnalyzer.
"""

from __future__ import annotations

from uuid import uuid4

from athena.knowledge.acquisition.domain.knowledge_representation import (
    KnowledgeRepresentation,
)

from athena.knowledge.intelligence import (
    StructureAnalyzer,
)


def test_structure_analyzer_detects_nodes() -> None:
    """Analyzer converts nodes into structure."""

    representation = KnowledgeRepresentation(
        title="Test Document",
    )

    representation.add_node(
        uuid4(),
    )

    representation.add_node(
        uuid4(),
    )

    analyzer = StructureAnalyzer()

    result = analyzer.analyze(
        representation,
    )

    assert len(result) == 2

    assert (
        result[0].node_type
        == "section"
    )