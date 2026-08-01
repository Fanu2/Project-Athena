"""
Athena Citation Repository Contract
"""

from abc import ABC, abstractmethod
from uuid import UUID

from athena.knowledge.acquisition.domain.citation_record import (
    CitationRecord,
)


class CitationRepository(ABC):
    """
    Repository abstraction for citations.
    """

    @abstractmethod
    def save(
        self,
        citation: CitationRecord,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_all(
        self,
    ) -> list[CitationRecord]:
        raise NotImplementedError

    @abstractmethod
    def find_by_evidence(
        self,
        evidence_id: UUID,
    ) -> list[CitationRecord]:
        raise NotImplementedError