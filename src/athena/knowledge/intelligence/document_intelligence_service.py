"""
Document intelligence application service.
"""

from __future__ import annotations

from athena.domain.document import Document

from athena.knowledge.acquisition.domain.knowledge_representation import (
    KnowledgeRepresentation,
)

from athena.knowledge.intelligence.document_analyzer import (
    DocumentAnalyzer,
)

from athena.knowledge.intelligence.document_intelligence import (
    DocumentIntelligence,
)

from athena.knowledge.intelligence.metadata_analyzer import (
    MetadataAnalyzer,
)

from athena.knowledge.intelligence.structure_analyzer import (
    StructureAnalyzer,
)

from athena.knowledge.intelligence.evidence_analyzer import (
    EvidenceAnalyzer,
)


class DocumentIntelligenceService:
    """
    Orchestrates document intelligence analysis.
    """

    def __init__(
        self,
        analyzer: DocumentAnalyzer | None = None,
        structure_analyzer: StructureAnalyzer | None = None,
        metadata_analyzer: MetadataAnalyzer | None = None,
        evidence_analyzer: EvidenceAnalyzer | None = None,
    ) -> None:
        """Initialize service."""

        self._analyzer = (
            analyzer
            if analyzer is not None
            else DocumentAnalyzer()
        )

        self._structure = (
            structure_analyzer
            if structure_analyzer is not None
            else StructureAnalyzer()
        )

        self._metadata = (
            metadata_analyzer
            if metadata_analyzer is not None
            else MetadataAnalyzer()
        )

        self._evidence = (
            evidence_analyzer
            if evidence_analyzer is not None
            else EvidenceAnalyzer()
        )

    def analyze(
        self,
        document: Document,
        representation: KnowledgeRepresentation,
    ) -> DocumentIntelligence:
        """
        Generate complete document intelligence.
        """

        return DocumentIntelligence(
            profile=self._analyzer.analyze(
                document,
                representation,
            ),
            metadata=self._metadata.analyze(
                document,
            ),
            structure=self._structure.analyze(
                representation,
            ),
            evidence=self._evidence.analyze(
                document,
            ),
        )