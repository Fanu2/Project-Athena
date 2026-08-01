"""
Relationship build pass tests.
"""

from athena.knowledge.acquisition.pipeline.relationship_build_pass import (
    RelationshipBuildPass,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)

from athena.knowledge.acquisition.domain.knowledge_candidate_relationship import (
    KnowledgeCandidateRelationship,
)

from athena.knowledge.repositories.relationships.memory_relationship_repository import (
    MemoryRelationshipRepository,
)


def test_relationship_build_persists():

    repository = (
        MemoryRelationshipRepository()
    )

    context = KnowledgeContext()

    context.add_service(
        "relationship_repository",
        repository,
    )

    candidate = KnowledgeCandidateRelationship(
        relationship_type="references",
        confidence=0.8,
    )

    result = RelationshipBuildPass().execute(
        context,
        [candidate],
    )

    assert len(result) == 1

    stored = repository.list_all()

    assert len(stored) == 1

    assert (
        stored[0].relationship_type
        == "references"
    )