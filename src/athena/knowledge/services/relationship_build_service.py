"""
Athena Relationship Build Service

Converts candidate relationships into
canonical knowledge relationships.
"""

from athena.knowledge.acquisition.domain.knowledge_candidate_relationship import (
    KnowledgeCandidateRelationship,
)

from athena.knowledge.acquisition.domain.knowledge_relationship import (
    KnowledgeRelationship,
)

from athena.knowledge.repositories.relationship_repository import (
    RelationshipRepository,
)


class RelationshipBuildService:
    """
    Builds and persists canonical relationships.
    """

    def __init__(
        self,
        repository: RelationshipRepository,
    ) -> None:

        self._repository = repository


    def build(
        self,
        candidates: list[
            KnowledgeCandidateRelationship
        ],
    ) -> list[KnowledgeRelationship]:
        """
        Convert candidate relationships.
        """

        relationships = []

        for candidate in candidates:

            relationship = KnowledgeRelationship(
                relationship_type=(
                    candidate.relationship_type
                ),
                confidence=(
                    candidate.confidence
                ),
                metadata=(
                    candidate.metadata.copy()
                ),
            )

            self._repository.save(
                relationship
            )

            relationships.append(
                relationship
            )

        return relationships