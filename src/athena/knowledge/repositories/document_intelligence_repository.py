"""
Athena Document Intelligence Repository Contract.
"""

from abc import ABC, abstractmethod

from athena.knowledge.intelligence.document_intelligence import (
    DocumentIntelligence,
)


class DocumentIntelligenceRepository(ABC):
    """
    Repository abstraction for document intelligence.
    """

    @abstractmethod
    def save(
        self,
        document_id: str,
        intelligence: DocumentIntelligence,
    ) -> None:
        """
        Store document intelligence.
        """
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        document_id: str,
    ) -> DocumentIntelligence | None:
        """
        Retrieve document intelligence.
        """
        raise NotImplementedError
