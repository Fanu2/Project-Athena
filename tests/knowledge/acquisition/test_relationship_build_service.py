"""
Relationship build service tests.
"""

from athena.knowledge.services.relationship_build_service import (
    RelationshipBuildService,
)

from athena.knowledge.repositories.relationships.memory_relationship_repository import (
    MemoryRelationshipRepository,
)

from athena.knowledge.acquisition.domain.knowledge_candidate_relationship import (
    KnowledgeCandidateRelationship,
)


def test_relationship_build_service():

    repository = (
        MemoryRelationshipRepository()
    )

    service = RelationshipBuildService(
        repository
    )

    candidate = (
        KnowledgeCandidateRelationship(
            relationship_type="references",
            confidence=0.8,
        )
    )

    result = service.build(
        [candidate]
    )

    assert len(result) == 1

    stored = repository.list_all()

    assert len(stored) == 1

    assert (
        stored[0].relationship_type
        == "references"
    )