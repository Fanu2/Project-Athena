"""
Workspace graph integration tests.
"""

from athena.services.knowledge_workspace_service import (
    KnowledgeWorkspaceService,
)

from athena.knowledge.services.knowledge_graph_service import (
    KnowledgeGraphService,
)

from athena.knowledge.repositories.relationships.memory_relationship_repository import (
    MemoryRelationshipRepository,
)

from athena.knowledge.repositories.memory.memory_repository import (
    MemoryKnowledgeRepository,
)

from athena.knowledge.services.knowledge_service import (
    KnowledgeService,
)

from athena.knowledge.acquisition.domain.knowledge_relationship import (
    KnowledgeRelationship,
)


def test_workspace_exposes_graph():

    relationship_repository = (
        MemoryRelationshipRepository()
    )

    graph_service = (
        KnowledgeGraphService(
            relationship_repository
        )
    )

    relationship_repository.save(
        KnowledgeRelationship(
            relationship_type="references"
        )
    )

    workspace = (
        KnowledgeWorkspaceService(
            KnowledgeService(
                MemoryKnowledgeRepository()
            ),
            graph_service,
        )
    )

    relationships = (
        workspace.get_relationships()
    )

    assert len(relationships) == 1

    assert (
        relationships[0]
        .relationship_type
        == "references"
    )