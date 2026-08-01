"""
Memory Evidence Repository
"""

from uuid import UUID

from athena.knowledge.acquisition.domain.evidence_record import (
    EvidenceRecord,
)

from athena.knowledge.repositories.evidence_repository import (
    EvidenceRepository,
)


class MemoryEvidenceRepository(
    EvidenceRepository
):
    """
    In-memory evidence storage.
    """

    def __init__(
        self,
    ) -> None:

        self._items: list[
            EvidenceRecord
        ] = []

    def save(
        self,
        evidence: EvidenceRecord,
    ) -> None:

        self._items.append(
            evidence
        )

    def list_all(
        self,
    ) -> list[EvidenceRecord]:

        return self._items

    def find_by_object(
        self,
        object_id: UUID,
    ) -> list[EvidenceRecord]:

        return [
            item
            for item in self._items
            if item.object_id == object_id
        ]