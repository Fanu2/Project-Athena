"""
Evidence adapter.

Bridges Document Intelligence evidence
into Athena knowledge evidence records.
"""

from __future__ import annotations

from athena.knowledge.acquisition.domain.evidence_record import (
    EvidenceRecord,
)

from athena.knowledge.intelligence.evidence_profile import (
    EvidenceProfile,
)


class EvidenceAdapter:
    """
    Converts Document Intelligence evidence
    into canonical Athena EvidenceRecord objects.
    """

    def to_record(
        self,
        profile: EvidenceProfile,
    ) -> EvidenceRecord:
        """
        Convert evidence profile into record.
        """

        return EvidenceRecord(
            source_id=profile.source_document,
            source_reference=profile.location,
            location=profile.location,
            extraction_method=(
                profile.evidence_type
            ),
            confidence=profile.confidence,
            metadata={
                "content": profile.content,
                **profile.metadata,
            },
        )