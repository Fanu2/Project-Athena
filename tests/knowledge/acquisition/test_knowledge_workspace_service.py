"""
Knowledge Workspace Service tests.
"""

from athena.services.knowledge_workspace_service import (
    KnowledgeWorkspaceService,
)

from athena.knowledge.services.knowledge_service import (
    KnowledgeService,
)

from athena.knowledge.repositories.memory.memory_repository import (
    MemoryKnowledgeRepository,
)

from athena.knowledge.acquisition.domain.knowledge_object import (
    KnowledgeObject,
)


def test_workspace_service_lists_knowledge():

    repository = (
        MemoryKnowledgeRepository()
    )

    knowledge_service = KnowledgeService(
        repository
    )

    workspace_service = (
        KnowledgeWorkspaceService(
            knowledge_service
        )
    )

    knowledge_service.save(
        KnowledgeObject(
            object_type="document",
            title="Workspace Knowledge",
        )
    )

    result = (
        workspace_service.list_knowledge()
    )

    assert len(result) == 1

    assert (
        result[0].title
        == "Workspace Knowledge"
    )