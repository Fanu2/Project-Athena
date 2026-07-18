"""
Application context.

Creates and owns shared application services.
"""

from __future__ import annotations

from pathlib import Path

from athena.ai.embeddings.repository import (
    EmbeddingRepository,
)
from athena.ai.embeddings.service import (
    EmbeddingService,
)
from athena.ai.llm.ollama import (
    OllamaProvider,
)
from athena.ai.rag.context_builder import (
    ContextBuilder,
)
from athena.ai.rag.service import (
    RAGService,
)
from athena.ai.retrieval.service import (
    RetrievalService,
)
from athena.bookmarks.service import BookmarkService
from athena.documents.service import DocumentService
from athena.indexing.repositories.sqlite import (
    SQLiteChunkRepository,
)
from athena.indexing.service import IndexingService
from athena.notes.service import NoteService
from athena.presentation.actions.workspace_actions import (
    WorkspaceActions,
)
from athena.search.search_service import SearchService
from athena.services.workspace_document_service import (
    WorkspaceDocumentService,
)


class ApplicationContext:
    """Owns application-wide services."""

    def __init__(self) -> None:
        """Initialize application services."""

        self.workspace_actions = WorkspaceActions()

        self.indexing_service: IndexingService | None = None

        self.search_service: SearchService | None = None

        self.document_service: WorkspaceDocumentService | None = None

        self.bookmark_service: BookmarkService | None = None

        self.note_service: NoteService | None = None

        self.rag_service: RAGService | None = None

    def open_workspace(
        self,
        workspace_path: Path,
    ) -> None:
        """Initialize workspace-specific services."""

        athena_directory = workspace_path / ".athena"

        athena_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        chunk_repository = SQLiteChunkRepository(
            athena_directory / "index.db",
        )

        embedding_repository = EmbeddingRepository(
            athena_directory / "embeddings.db",
        )

        self.indexing_service = IndexingService(
            chunk_repository,
        )

        self.search_service = SearchService(
            chunk_repository,
        )

        embedding_service = EmbeddingService()

        retrieval_service = RetrievalService(
            embedding_service=embedding_service,
            embedding_repository=embedding_repository,
            chunk_repository=chunk_repository,
        )

        self.rag_service = RAGService(
            retrieval_service=retrieval_service,
            context_builder=ContextBuilder(),
            llm_provider=OllamaProvider(),
            model_name="mistral",
        )

        self.bookmark_service = BookmarkService(
            athena_directory / "bookmarks.json",
        )

        self.note_service = NoteService(
            athena_directory / "notes.json",
        )

        document_service = DocumentService(
            workspace_path / "documents",
        )

        self.document_service = WorkspaceDocumentService(
            document_service=document_service,
            indexing_service=self.indexing_service,
        )

    def close_workspace(self) -> None:
        """Release workspace-specific services."""

        self.document_service = None

        self.indexing_service = None

        self.search_service = None

        self.bookmark_service = None

        self.note_service = None

        self.rag_service = None
