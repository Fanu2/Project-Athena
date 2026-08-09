"""
Citation adapter.

Bridges Athena document intelligence
evidence into citation records.
"""

from __future__ import annotations

from athena.knowledge.acquisition.domain.citation_record import (
    CitationRecord,
)

from athena.knowledge.acquisition.domain.evidence_record import (
    EvidenceRecord,
)


class CitationAdapter:
    """
    Converts EvidenceRecord objects into
    CitationRecord objects.
    """

    def to_record(
        self,
        evidence: EvidenceRecord,
    ) -> CitationRecord:
        """
        Create citation from evidence.
        """

        return CitationRecord(
            evidence_id=evidence.evidence_id,
            source_reference=(
                evidence.source_reference
            ),
            citation_text=(
                evidence.metadata.get(
                    "content",
                )
            ),
            location=evidence.location,
            confidence=evidence.confidence,
            metadata={
                "extraction_method": (
                    evidence.extraction_method
                ),
                "provider": evidence.provider,
                **evidence.metadata,
            },
        )