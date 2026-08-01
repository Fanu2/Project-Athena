"""
Workspace document knowledge import integration tests.
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
    Fake workspace document service.
    """

    documents_dir = Path("workspace")

    def import_document(
        self,
        source,
    ):
        return source


class FakeIndexingService:
    """
    Fake indexing service.
    """

    def index_document(
        self,
        document_path,
        force=False,
    ):
        return None


class FakeCompiler:
    """
    Fake knowledge compiler.

    Records invocation.
    """

    def __init__(self):
        self.called = False

    def compile_document(
        self,
        document,
        context,
    ):
        self.called = True
        return []


def test_workspace_import_invokes_knowledge_compiler():

    context = KnowledgeContext()

    compiler = FakeCompiler()

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

    assert compiler.called is True