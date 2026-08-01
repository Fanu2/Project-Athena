"""
Athena Knowledge Relationship Repository Contract

Persistence abstraction for semantic
connections between knowledge objects.
"""

from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from athena.knowledge.acquisition.domain.knowledge_relationship import (
    KnowledgeRelationship,
)


class RelationshipRepository(ABC):
    """
    Repository contract for knowledge relationships.
    """

    @abstractmethod
    def save(
        self,
        relationship: KnowledgeRelationship,
    ) -> None:
        """
        Persist relationship.
        """

    @abstractmethod
    def get(
        self,
        relationship_id: UUID,
    ) -> KnowledgeRelationship | None:
        """
        Retrieve relationship.
        """

    @abstractmethod
    def list_all(
        self,
    ) -> List[KnowledgeRelationship]:
        """
        Return all relationships.
        """

    @abstractmethod
    def find_by_source(
        self,
        object_id: UUID,
    ) -> List[KnowledgeRelationship]:
        """
        Find outgoing relationships.
        """