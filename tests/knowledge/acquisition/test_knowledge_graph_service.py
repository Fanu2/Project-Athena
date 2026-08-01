"""
Knowledge Graph Service tests.
"""

from athena.knowledge.services.knowledge_graph_service import (
    KnowledgeGraphService,
)

from athena.knowledge.repositories.relationships.memory_relationship_repository import (
    MemoryRelationshipRepository,
)

from athena.knowledge.acquisition.domain.knowledge_relationship import (
    KnowledgeRelationship,
)


def test_graph_service_lists_relationships():

    repository = (
        MemoryRelationshipRepository()
    )

    service = KnowledgeGraphService(
        repository
    )

    relationship = KnowledgeRelationship(
        relationship_type="references",
    )

    repository.save(
        relationship
    )

    result = (
        service.list_relationships()
    )

    assert len(result) == 1

    assert (
        result[0].relationship_type
        == "references"
    )