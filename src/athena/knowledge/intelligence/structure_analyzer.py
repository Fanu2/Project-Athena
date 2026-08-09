"""
Document structure analyzer.
"""

from __future__ import annotations

from athena.knowledge.acquisition.domain.knowledge_representation import (
    KnowledgeRepresentation,
)

from athena.knowledge.intelligence.document_structure import (
    DocumentStructureNode,
)


class StructureAnalyzer:
    """
    Analyze document representation structure.
    """

    def analyze(
        self,
        representation: KnowledgeRepresentation,
    ) -> list[DocumentStructureNode]:
        """
        Convert representation nodes into
        structure intelligence nodes.
        """

        return [
            DocumentStructureNode(
                node_type="section",
                level=0,
            )
            for _ in representation.nodes
        ]