"""
Full Athena knowledge lifecycle tests.
"""

from athena.knowledge.acquisition.engine.knowledge_acquisition_engine import (
    KnowledgeAcquisitionEngine,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)

from athena.knowledge.repositories.memory.memory_repository import (
    MemoryKnowledgeRepository,
)

from athena.knowledge.services.knowledge_service import (
    KnowledgeService,
)

from athena.services.knowledge_workspace_service import (
    KnowledgeWorkspaceService,
)


def test_document_to_workspace_lifecycle():

    context = KnowledgeContext()

    repository = (
        MemoryKnowledgeRepository()
    )

    context.add_service(
        "knowledge_repository",
        repository,
    )

    #
    # Existing compiler integration
    #

    engine = KnowledgeAcquisitionEngine()

    #
    # No provider here:
    # verifies safe empty path
    #

    result = engine.compile(
        "demo.pdf",
        context,
    )

    assert result is not None

    #
    # Workspace layer
    #

    workspace = (
        KnowledgeWorkspaceService(
            KnowledgeService(
                repository
            )
        )
    )

    items = (
        workspace
        .list_workspace_items()
    )

    assert items is not None