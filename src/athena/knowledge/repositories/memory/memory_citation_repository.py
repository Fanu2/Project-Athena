"""
Memory Citation Repository
"""

from uuid import UUID

from athena.knowledge.acquisition.domain.citation_record import (
    CitationRecord,
)

from athena.knowledge.repositories.citation_repository import (
    CitationRepository,
)


class MemoryCitationRepository(
    CitationRepository
):
    """
    In-memory citation storage.
    """

    def __init__(
        self,
    ) -> None:

        self._items: list[
            CitationRecord
        ] = []

    def save(
        self,
        citation: CitationRecord,
    ) -> None:

        self._items.append(
            citation
        )

    def list_all(
        self,
    ) -> list[CitationRecord]:

        return self._items

    def find_by_evidence(
        self,
        evidence_id: UUID,
    ) -> list[CitationRecord]:

        return [
            item
            for item in self._items
            if item.evidence_id == evidence_id
        ]