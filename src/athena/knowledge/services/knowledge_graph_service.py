"""
Athena Knowledge Graph Service

Provides graph traversal operations
over knowledge relationships.
"""

from uuid import UUID

from athena.knowledge.acquisition.domain.knowledge_relationship import (
    KnowledgeRelationship,
)

from athena.knowledge.repositories.relationship_repository import (
    RelationshipRepository,
)


class KnowledgeGraphService:
    """
    Application service for knowledge graph queries.
    """

    def __init__(
        self,
        repository: RelationshipRepository,
    ) -> None:

        self._repository = repository

    def list_relationships(
        self,
    ) -> list[KnowledgeRelationship]:
        """
        Return all relationships.
        """

        return (
            self._repository
            .list_all()
        )

    def get_outgoing(
        self,
        object_id: UUID,
    ) -> list[KnowledgeRelationship]:
        """
        Return relationships where object
        is the source.
        """

        return (
            self._repository
            .find_by_source(
                object_id
            )
        )

    def find_related(
        self,
        object_id: UUID,
    ) -> list[KnowledgeRelationship]:
        """
        Find directly related knowledge.
        """

        return self.get_outgoing(
            object_id
        )