"""
Athena Memory Relationship Repository
"""

from uuid import UUID

from athena.knowledge.acquisition.domain.knowledge_relationship import (
    KnowledgeRelationship,
)

from ..relationship_repository import (
    RelationshipRepository,
)


class MemoryRelationshipRepository(
    RelationshipRepository
):
    """
    In-memory relationship storage.
    """

    def __init__(self) -> None:

        self._relationships = {}


    def save(
        self,
        relationship: KnowledgeRelationship,
    ) -> None:

        self._relationships[
            relationship.relationship_id
        ] = relationship


    def get(
        self,
        relationship_id: UUID,
    ) -> KnowledgeRelationship | None:

        return self._relationships.get(
            relationship_id
        )


    def list_all(
        self,
    ) -> list[KnowledgeRelationship]:

        return list(
            self._relationships.values()
        )


    def find_by_source(
        self,
        object_id: UUID,
    ) -> list[KnowledgeRelationship]:

        return [
            r
            for r in self._relationships.values()
            if r.source_object_id
            == object_id
        ]