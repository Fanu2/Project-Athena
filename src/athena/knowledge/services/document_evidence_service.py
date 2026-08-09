"""
Athena Document Evidence Service.

Connects Document Intelligence evidence
with persistent Athena evidence storage.
"""

from __future__ import annotations

from athena.domain.document import Document

from athena.knowledge.intelligence.evidence_analyzer import (
    EvidenceAnalyzer,
)

from athena.knowledge.intelligence.evidence_adapter import (
    EvidenceAdapter,
)

from athena.knowledge.services.evidence_build_service import (
    EvidenceBuildService,
)


class DocumentEvidenceService:
    """
    Builds persistent evidence from documents.
    """

    def __init__(
        self,
        builder: EvidenceBuildService,
        analyzer: EvidenceAnalyzer | None = None,
        adapter: EvidenceAdapter | None = None,
    ) -> None:

        self._builder = builder

        self._analyzer = (
            analyzer
            if analyzer is not None
            else EvidenceAnalyzer()
        )

        self._adapter = (
            adapter
            if adapter is not None
            else EvidenceAdapter()
        )

    def build(
        self,
        document: Document,
    ) -> list:

        profiles = (
            self._analyzer.analyze(
                document,
            )
        )

        records = []

        for profile in profiles:

            record = (
                self._adapter.to_record(
                    profile,
                )
            )

            self._builder.build_record(
                record,
            )

            records.append(
                record,
            )

        return records