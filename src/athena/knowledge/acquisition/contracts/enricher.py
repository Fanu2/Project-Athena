"""
Athena Enricher Contract

Defines enrichment operations applied to
validated Knowledge Objects.
"""

from abc import ABC, abstractmethod

from ..domain.knowledge_object import KnowledgeObject
from ..domain.knowledge_context import KnowledgeContext


class Enricher(ABC):
    """
    Base contract for Knowledge Object enrichment.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Enricher identifier.
        """
        pass

    @property
    @abstractmethod
    def capabilities(self) -> list[str]:
        """
        Supported enrichment capabilities.

        Examples:
            embedding
            summary
            keywords
            classification
        """
        pass

    @abstractmethod
    def enrich(
        self,
        obj: KnowledgeObject,
        context: KnowledgeContext,
    ) -> KnowledgeObject:
        """
        Enrich a Knowledge Object.

        Returns the enriched object.
        """
        pass