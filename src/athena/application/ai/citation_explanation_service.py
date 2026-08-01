"""
Citation explanation service.

Converts runtime citations into
user-understandable citation explanations.
"""

from __future__ import annotations

from athena.domain.ai.citation import Citation
from athena.domain.ai.evidence_record import EvidenceRecord
from athena.domain.ai.resolved_citation import ResolvedCitation


class CitationExplanationService:
    """
    Explain why citations were selected.
    """

    def resolve(
        self,
        citations: list[Citation],
        evidence: list[EvidenceRecord],
    ) -> list[ResolvedCitation]:
        """
        Build resolved citations from citations and evidence.
        """

        resolved: list[ResolvedCitation] = []

        for citation, record in zip(
            citations,
            evidence,
            strict=False,
        ):
            resolved.append(
                ResolvedCitation(
                    document_name=citation.document_name,
                    page=citation.page,
                    snippet=citation.snippet,
                    score=citation.score,
                    reasons=record.ranking_reasons,
                )
            )

        return resolved