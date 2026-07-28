"""
Citation service.
"""

from __future__ import annotations

from uuid import UUID

from athena.domain.ai.citation import Citation
from athena.domain.ai.evidence_record import EvidenceRecord


class CitationService:
    """Convert evidence records into citations."""

    def create_citations(
        self,
        evidence_records: list[EvidenceRecord],
    ) -> list[Citation]:
        """Create citations from evidence."""

        citations: list[Citation] = []

        for evidence in evidence_records:

            try:
                document_id = UUID(
                    evidence.document_id,
                )
            except ValueError:
                document_id = UUID(
                    int=0,
                )

            citations.append(
                Citation(
                    document_id=document_id,
                    document_name=evidence.document_name,
                    page=evidence.page,
                    snippet=evidence.text,
                    score=evidence.final_score,
                    chunk_id=evidence.chunk_id,
                    ranking_reasons=evidence.ranking_reasons,
                )
            )

        return citations