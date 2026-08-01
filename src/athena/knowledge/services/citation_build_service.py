"""
Athena Citation Build Service

Creates citation records from evidence.
"""

from athena.knowledge.acquisition.domain.evidence_record import (
    EvidenceRecord,
)

from athena.knowledge.acquisition.domain.citation_record import (
    CitationRecord,
)

from athena.knowledge.repositories.citation_repository import (
    CitationRepository,
)


class CitationBuildService:
    """
    Builds and stores citation records.
    """

    def __init__(
        self,
        repository: CitationRepository,
    ) -> None:

        self._repository = repository

    def build(
        self,
        evidence: EvidenceRecord,
    ) -> CitationRecord:
        """
        Create citation from evidence.
        """

        citation = CitationRecord(
            evidence_id=(
                evidence.evidence_id
            ),
            source_reference=(
                evidence.source_reference
            ),
            citation_text=(
                evidence.source_reference
            ),
            location=(
                evidence.location
            ),
            confidence=(
                evidence.confidence
            ),
            metadata={
                "provider": evidence.provider,
                "extraction_method": (
                    evidence.extraction_method
                ),
            },
        )

        self._repository.save(
            citation
        )

        return citation