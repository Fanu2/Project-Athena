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

from athena.ai.intent.service import (
    IntentService,
)

from athena.ai.llm.conversation_context_enricher import (
    ConversationContextEnricher,
)

from athena.ai.llm.conversation_execution_service import (
    ConversationExecutionService,
)

from athena.ai.llm.execution_service import (
    ExecutionService,
)

from athena.ai.llm.ollama import (
    OllamaProvider,
)

from athena.ai.llm.rag_knowledge_context import (
    RAGKnowledgeContext,
)

from athena.ai.llm.runtime_bootstrap import (
    LLMRuntimeBootstrap,
)

from athena.ai.llm.runtime_router import (
    RuntimeRouter,
)

from athena.ai.metadata.service import (
    MetadataService,
)

from athena.ai.rag.context_builder import (
    ContextBuilder,
)

from athena.ai.rag.service import (
    RAGService,
)

from athena.ai.retrieval.service import (
    RetrievalService as SemanticRetrievalService,
)

from athena.application.ai.retrieval_service import (
    RetrievalService,
)

from athena.application.conversation.conversation_query_service import (
    ConversationQueryService,
)

from athena.application.viewer import (
    DocumentViewerService,
)

from athena.bookmarks.service import (
    BookmarkService,
)

from athena.conversation.service import (
    ConversationService,
)

from athena.documents.service import (
    DocumentService,
)

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

from athena.services.athena_query_service import (
    AthenaQueryService,
)

from athena.services.workspace_document_service import (
    WorkspaceDocumentService,
)

from athena.services.workspace_query_service import (
    WorkspaceQueryService,
)

from athena.settings import (
    AISettingsService,
    LLMSettings,
)

from athena.workspace.models import (
    Workspace,
)

from athena.workspace.service import (
    WorkspaceService,
)


class ApplicationContext:
    """Owns application-wide services."""

    def __init__(self) -> None:
        """Initialize application services."""

        self.workspace_actions = WorkspaceActions()

        self.indexing_service: IndexingService | None = None

        self.indexed_document_service: (
            IndexedDocumentService | None
        ) = None

        self.search_service: SearchService | None = None

        self.document_service: (
            WorkspaceDocumentService | None
        ) = None

        self.document_viewer_service = DocumentViewerService()

        self.bookmark_service: BookmarkService | None = None

        self.note_service: NoteService | None = None

        self.workspace_service = WorkspaceService()

        self.current_workspace: Workspace | None = None

        #
        # Settings
        #

        self.ai_settings_service: (
            AISettingsService | None
        ) = None

        self.llm_settings: (
            LLMSettings | None
        ) = None

        #
        # AI services
        #

        self.metadata_service: (
            MetadataService | None
        ) = None

        self.retrieval_service: (
            RetrievalService | None
        ) = None

        self.rag_service: (
            RAGService | None
        ) = None

        #
        # Query services
        #

        self.athena_query_service: (
            AthenaQueryService | None
        ) = None

        self.conversation_query_service: (
            ConversationQueryService | None
        ) = None

        #
        # Conversation services
        #

        self.conversation_service: (
            ConversationService | None
        ) = None

        self.conversation_execution_service: (
            ConversationExecutionService | None
        ) = None

        #
        # LLM runtime services (A2.22)
        #

        self.llm_runtime_bootstrap: (
            LLMRuntimeBootstrap | None
        ) = None

        self.runtime_router: (
            RuntimeRouter | None
        ) = None

        self.execution_service: (
            ExecutionService | None
        ) = None

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

        intent_service = IntentService()

        self.metadata_service = MetadataService(
            document_titles=(),
        )

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

        semantic_retrieval_service = SemanticRetrievalService(
            embedding_service=embedding_service,
            embedding_repository=embedding_repository,
            chunk_repository=chunk_repository,
        )

        self.retrieval_service = RetrievalService(
            semantic_retrieval_service=semantic_retrieval_service,
        )

        #
        # Conversation knowledge enrichment
        #

        knowledge_context = RAGKnowledgeContext(
            self.retrieval_service,
        )

        conversation_enricher = ConversationContextEnricher(
            knowledge_context,
        )

        #
        # LLM runtime initialization
        #

        self.llm_runtime_bootstrap = (
            LLMRuntimeBootstrap()
        )

        model_manager = (
            self.llm_runtime_bootstrap.initialize()
        )

        self.runtime_router = RuntimeRouter(
            model_manager=model_manager,
        )

        self.execution_service = ExecutionService(
            router=self.runtime_router,
        )

        #
        # Conversation execution
        #

        self.conversation_execution_service = (
            ConversationExecutionService(
                enricher=conversation_enricher,
                executor=self.execution_service,
            )
        )

        #
        # RAG answer generation
        #

        context_builder = ContextBuilder(
            document_service=document_service,
        )

        self.rag_service = RAGService(
            retrieval_service=self.retrieval_service,
            context_builder=context_builder,
            llm_provider=OllamaProvider(),
            intent_service=intent_service,
            metadata_service=self.metadata_service,
            model_name=self.llm_settings.model,
        )

        self.athena_query_service = AthenaQueryService(
            rag_service=self.rag_service,
            workspace_service=WorkspaceQueryService(
                self.indexed_document_service,
            ),
        )

        self.conversation_query_service = ConversationQueryService(
            conversation_service=self.conversation_service,
            query_service=self.athena_query_service,
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

        if self.current_workspace is not None and self.conversation_service is not None:
            self.conversation_service.save(
                self.current_workspace.path / ".athena" / "conversation.json",
            )

        self.document_service = None

        self.indexing_service = None

        self.indexed_document_service = None

        self.search_service = None

        self.bookmark_service = None

        self.note_service = None

        self.rag_service = None

        self.athena_query_service = None
        self.conversation_query_service = None

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

