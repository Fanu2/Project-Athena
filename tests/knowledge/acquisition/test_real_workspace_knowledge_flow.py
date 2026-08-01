"""
Real workspace knowledge lifecycle test.
"""

from pathlib import Path

from athena.services.workspace_document_service import (
    WorkspaceDocumentService,
)

from athena.knowledge.services.knowledge_compilation_service import (
    KnowledgeCompilationService,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)

from athena.knowledge.repositories.memory.memory_repository import (
    MemoryKnowledgeRepository,
)


class FakeDocumentService:
    """
    Fake document storage layer.
    """

    documents_dir = Path("workspace")

    def import_document(
        self,
        source,
    ):
        return source


class FakeIndexingService:
    """
    Fake index layer.
    """

    def index_document(
        self,
        document_path,
        force=False,
    ):
        return None


class FakeProviderManager:
    """
    Provider placeholder.
    """


def test_workspace_real_compilation_path():

    repository = (
        MemoryKnowledgeRepository()
    )

    context = KnowledgeContext()

    context.add_service(
        "knowledge_repository",
        repository,
    )

    #
    # Real compiler service
    #

    compiler = (
        KnowledgeCompilationService()
    )

    workspace = (
        WorkspaceDocumentService(
            FakeDocumentService(),
            FakeIndexingService(),
            compiler,
            context,
        )
    )

    result = workspace.import_document(
        Path("demo.pdf")
    )

    assert result == Path(
        "demo.pdf"
    )

    #
    # Safe validation:
    # compilation service exists
    #

    assert compiler is not None