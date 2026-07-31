"""
Athena Relationship Extractor Contract

Defines extraction of semantic relationships
between knowledge entities.
"""

from abc import ABC, abstractmethod

from ..domain.knowledge_context import KnowledgeContext
from ..domain.knowledge_candidate import KnowledgeCandidate
from ..domain.knowledge_relationship import KnowledgeRelationship


class RelationshipExtractor(ABC):
    """
    Base contract for relationship extraction.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Relationship extractor identifier.
        """
        pass

    @property
    @abstractmethod
    def supported_relationships(self) -> list[str]:
        """
        Relationship types supported.
        """
        pass

    @abstractmethod
    def extract_relationships(
        self,
        candidates: list[KnowledgeCandidate],
        context: KnowledgeContext,
    ) -> list[KnowledgeRelationship]:
        """
        Extract semantic relationships.
        """
        pass