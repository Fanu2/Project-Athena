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

from athena.indexing.repositories.sqlite_document import (
    SQLiteDocumentRepository,
)

from athena.indexing.service import (
    IndexingService,
)

from athena.indexing.services.indexed_document_service import (
    IndexedDocumentService,
)

from athena.notes.service import (
    NoteService,
)

from athena.presentation.actions.workspace_actions import (
    WorkspaceActions,
)

from athena.search.search_service import (
    SearchService,
)

from athena.services.workspace_document_service import (
    WorkspaceDocumentService,
)

from athena.services.workspace_query_service import (
    WorkspaceQueryService,
)

from athena.services.athena_query_service import (
    AthenaQueryService,
)

from athena.application.viewer import (
    DocumentViewerService,
)

from athena.settings import (
    AISettingsService,
    LLMSettings,
)
from athena.conversation.service import (
    ConversationService,
)

from athena.workspace.models import Workspace
from athena.workspace.service import WorkspaceService


class ApplicationContext:
    """Owns application-wide services."""

    def __init__(self) -> None:
        """Initialize application services."""

        self.workspace_actions = WorkspaceActions()

        self.indexing_service: IndexingService | None = None

        self.indexed_document_service: IndexedDocumentService | None = None

        self.search_service: SearchService | None = None

        self.document_service: WorkspaceDocumentService | None = None

        self.document_viewer_service = DocumentViewerService()

        self.bookmark_service: BookmarkService | None = None

        self.note_service: NoteService | None = None

        self.workspace_service = WorkspaceService()

        self.current_workspace: Workspace | None = None

        # Compatibility with GUI
        self.ai_settings_service: AISettingsService | None = None

        # New settings model
        self.llm_settings: LLMSettings | None = None

        self.rag_service: RAGService | None = None

        self.athena_query_service: AthenaQueryService | None = None

        self.conversation_service: ConversationService | None = None

    def open_workspace(
        self,
        workspace_path: Path,
    ) -> None:
        """Initialize workspace-specific services."""

        #
        # Load workspace metadata
        #

        workspace = self.workspace_service.open_workspace(
            workspace_path,
        )

        self.current_workspace = workspace

        workspace_path = workspace.path

        athena_directory = workspace_path / ".athena"

        athena_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        #
        # Conversation
        #

        self.conversation_service = ConversationService()

        self.conversation_service.load(
            athena_directory / "conversation.json",
        )

        #
        # Storage
        #

        chunk_repository = SQLiteChunkRepository(
            athena_directory / "index.db",
        )

        document_repository = SQLiteDocumentRepository(
            athena_directory / "index.db",
        )

        embedding_repository = EmbeddingRepository(
            athena_directory / "embeddings.db",
        )

        #
        # AI settings
        #

        self.ai_settings_service = AISettingsService(
            athena_directory / "settings" / "ai.json",
        )

        ai_settings = self.ai_settings_service.load()

        self.llm_settings = LLMSettings(
            model=ai_settings.default_model,
        )

        #
        # AI services
        #

        embedding_service = EmbeddingService()

        #
        # Indexing
        #

        self.indexing_service = IndexingService(
            repository=chunk_repository,
            index_repository=document_repository,
            document_library_repository=None,
            embedding_service=embedding_service,
            embedding_repository=embedding_repository,
        )

        self.indexed_document_service = IndexedDocumentService(
            document_repository,
        )

        #
        # Search
        #

        self.search_service = SearchService(
            chunk_repository,
        )

        #
        # Documents
        #

        document_service = DocumentService(
            workspace.path / "documents",
        )

        self.document_service = WorkspaceDocumentService(
            document_service=document_service,
            indexing_service=self.indexing_service,
        )

        #
        # RAG
        #

        retrieval_service = RetrievalService(
            embedding_service=embedding_service,
            embedding_repository=embedding_repository,
            chunk_repository=chunk_repository,
        )

        context_builder = ContextBuilder(
            document_service=document_service,
        )

        self.rag_service = RAGService(
            retrieval_service=retrieval_service,
            context_builder=context_builder,
            llm_provider=OllamaProvider(),
            model_name=self.llm_settings.model,
        )

        self.athena_query_service = AthenaQueryService(
            rag_service=self.rag_service,
            workspace_service=WorkspaceQueryService(
                self.indexed_document_service,
            ),
        )

        #
        # User data
        #

        self.bookmark_service = BookmarkService(
            athena_directory / "bookmarks.json",
        )

        self.note_service = NoteService(
            athena_directory / "notes.json",
        )


    def close_workspace(self) -> None:
        """Release workspace-specific services."""

        #
        # Save conversation
        #

        if (
            self.current_workspace is not None
            and self.conversation_service is not None
        ):
            self.conversation_service.save(
                self.current_workspace.path
                / ".athena"
                / "conversation.json",
            )

        self.document_service = None

        self.indexing_service = None

        self.indexed_document_service = None

        self.search_service = None

        self.bookmark_service = None

        self.note_service = None

        self.rag_service = None

        self.athena_query_service = None

        self.ai_settings_service = None

        self.llm_settings = None

        self.conversation_service = None

        self.current_workspace = None


    @property
    def workspace(self) -> Workspace:
        """Return the currently open workspace."""

        if self.current_workspace is None:
            raise RuntimeError(
                "No workspace is currently open.",
            )

        return self.current_workspace
