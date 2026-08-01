"""
Athena Citation Service

Application service exposing citations
for workspace features.
"""

from uuid import UUID

from athena.knowledge.acquisition.domain.citation_record import (
    CitationRecord,
)

from athena.knowledge.repositories.citation_repository import (
    CitationRepository,
)


class CitationService:
    """
    Provides citation lookup operations.
    """

    def __init__(
        self,
        repository: CitationRepository,
    ) -> None:

        self._repository = repository

    def list_citations(
        self,
    ) -> list[CitationRecord]:
        """
        Return all citations.
        """

        return (
            self._repository
            .list_all()
        )

    def find_by_evidence(
        self,
        evidence_id: UUID,
    ) -> list[CitationRecord]:
        """
        Find citations linked to evidence.
        """

        return (
            self._repository
            .find_by_evidence(
                evidence_id
            )
        )