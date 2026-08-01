"""
Knowledge Workspace Read Model tests.
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


def test_workspace_read_model():

    repository = (
        MemoryKnowledgeRepository()
    )

    workspace_service = (
        KnowledgeWorkspaceService(
            KnowledgeService(
                repository
            )
        )
    )

    repository.save(
        KnowledgeObject(
            object_type="document",
            title="Athena Document",
            confidence=0.90,
            metadata={
                "provider": "docling",
                "source_reference": "demo.pdf",
                "extraction_method": "pdf",
            },
        )
    )

    items = (
        workspace_service
        .list_workspace_items()
    )

    assert len(items) == 1

    item = items[0]

    assert (
        item.title
        == "Athena Document"
    )

    assert (
        item.object_type
        == "document"
    )

    assert (
        item.provider
        == "docling"
    )

    assert (
        item.source_reference
        == "demo.pdf"
    )

    assert (
        item.extraction_method
        == "pdf"
    )

    assert (
        item.confidence
        == 0.90
    )