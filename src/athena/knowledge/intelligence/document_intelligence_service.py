"""
Document intelligence application service.

Coordinates document analysis workflows.
"""

from __future__ import annotations

from athena.domain.document import Document

from athena.knowledge.acquisition.domain.knowledge_representation import (
    KnowledgeRepresentation,
)

from athena.knowledge.intelligence.document_analyzer import (
    DocumentAnalyzer,
)

from athena.knowledge.intelligence.document_profile import (
    DocumentProfile,
)


class DocumentIntelligenceService:
    """
    Application boundary for document intelligence.

    Coordinates intelligence generation while
    keeping domain models independent.
    """

    def __init__(
        self,
        analyzer: DocumentAnalyzer | None = None,
    ) -> None:
        """Initialize service."""

        self._analyzer = (
            analyzer
            if analyzer is not None
            else DocumentAnalyzer()
        )

    def analyze(
        self,
        document: Document,
        representation: KnowledgeRepresentation,
    ) -> DocumentProfile:
        """
        Analyze a document.

        Returns enriched document intelligence.
        """

        return self._analyzer.analyze(
            document,
            representation,
        )