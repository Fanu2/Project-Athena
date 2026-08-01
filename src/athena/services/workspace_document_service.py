"""
Workspace document service.

Coordinates document management,
indexing, and knowledge compilation.
"""

from __future__ import annotations

from pathlib import Path

from athena.documents.models import Document
from athena.documents.service import DocumentService
from athena.indexing.service import IndexingService

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)

from athena.knowledge.acquisition.runtime.knowledge_runtime_factory import (
    KnowledgeRuntimeFactory,
)

from athena.knowledge.services.knowledge_compilation_service import (
    KnowledgeCompilationService,
)


class WorkspaceDocumentService:
    """
    High-level document workflow.

    Coordinates:
    - document storage
    - indexing
    - knowledge compilation
    """

    def __init__(
        self,
        document_service: DocumentService,
        indexing_service: IndexingService,
        knowledge_compiler: KnowledgeCompilationService | None = None,
        knowledge_context: KnowledgeContext | None = None,
        runtime_factory: KnowledgeRuntimeFactory | None = None,
    ) -> None:
        """
        Initialize workspace document service.
        """

        self._documents = document_service

        self._indexing = indexing_service

        self._knowledge_compiler = (
            knowledge_compiler
        )

        if knowledge_context is not None:

            self._knowledge_context = (
                knowledge_context
            )

        elif runtime_factory is not None:

            self._knowledge_context = (
                runtime_factory.create_context()
            )

        else:

            self._knowledge_context = (
                KnowledgeContext()
            )

    @property
    def document_service(
        self,
    ) -> DocumentService:
        """
        Return underlying document service.
        """

        return self._documents

    @property
    def documents_dir(
        self,
    ) -> Path:
        """
        Return workspace documents directory.
        """

        return self._documents.documents_dir

    def list_documents(
        self,
    ) -> list[Document]:
        """
        Return all documents.
        """

        return (
            self._documents.list_documents()
        )

    def import_document(
        self,
        source: Path,
        force: bool = False,
    ) -> Path:
        """
        Import, index, and compile document knowledge.
        """

        document_path = (
            self._documents.import_document(
                source,
            )
        )

        self._indexing.index_document(
            document_path,
            force=force,
        )

        #
        # Athena Knowledge Compilation
        #

        if self._knowledge_compiler is not None:

            print(
                "AKC COMPILER ACTIVE:",
                type(
                    self._knowledge_compiler
                ).__name__,
            )

            print(
                "AKC KNOWLEDGE REPOSITORY:",
                self._knowledge_context.get_service(
                    "knowledge_repository"
                ),
            )

            self._knowledge_compiler.compile_document(
                str(document_path),
                self._knowledge_context,
            )

        else:

            print(
                "AKC COMPILER NOT CONFIGURED"
            )

        return document_path

    def import_folder(
        self,
        folder: Path,
        force: bool = False,
    ) -> list[Path]:
        """
        Import and index all supported documents.
        """

        imported_documents: list[Path] = []

        for source in (
            self._documents.discover_documents(
                folder,
            )
        ):

            imported_documents.append(
                self.import_document(
                    source,
                    force=force,
                )
            )

        return imported_documents

    def remove_document(
        self,
        document_path: Path,
    ) -> None:
        """
        Remove document.
        """

        self._documents.remove_document(
            document_path,
        )