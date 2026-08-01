"""
Athena Evidence Service

Application service exposing evidence
associated with knowledge objects.
"""

from uuid import UUID

from athena.knowledge.acquisition.domain.evidence_record import (
    EvidenceRecord,
)


class EvidenceService:
    """
    Provides evidence lookup operations.
    """

    def __init__(
        self,
        repository=None,
    ) -> None:

        self._repository = repository

    def list_evidence(
        self,
    ) -> list[EvidenceRecord]:
        """
        Return all evidence records.
        """

        if self._repository is None:
            return []

        return (
            self._repository
            .list_all()
        )

    def find_by_object(
        self,
        object_id: UUID,
    ) -> list[EvidenceRecord]:
        """
        Find evidence linked to a knowledge object.
        """

        if self._repository is None:
            return []

        return (
            self._repository
            .find_by_object(
                object_id
            )
        )