"""
Athena Evidence Repository Contract
"""

from abc import ABC, abstractmethod
from uuid import UUID

from athena.knowledge.acquisition.domain.evidence_record import (
    EvidenceRecord,
)


class EvidenceRepository(ABC):
    """
    Repository abstraction for evidence records.
    """

    @abstractmethod
    def save(
        self,
        evidence: EvidenceRecord,
    ) -> None:
        """
        Store evidence.
        """
        raise NotImplementedError

    @abstractmethod
    def list_all(
        self,
    ) -> list[EvidenceRecord]:
        """
        Return all evidence.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_object(
        self,
        object_id: UUID,
    ) -> list[EvidenceRecord]:
        """
        Find evidence for knowledge object.
        """
        raise NotImplementedError