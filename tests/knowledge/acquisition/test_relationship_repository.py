"""
Knowledge relationship repository tests.
"""

from athena.knowledge.repositories.relationships.memory_relationship_repository import (
    MemoryRelationshipRepository,
)

from athena.knowledge.acquisition.domain.knowledge_relationship import (
    KnowledgeRelationship,
)


def test_relationship_repository_save():

    repository = (
        MemoryRelationshipRepository()
    )

    relationship = KnowledgeRelationship(
        relationship_type="references"
    )

    repository.save(
        relationship
    )

    result = repository.get(
        relationship.relationship_id
    )

    assert result is not None

    assert (
        result.relationship_type
        == "references"
    )