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

from athena.knowledge.services.knowledge_compilation_service import (
    KnowledgeCompilationService,
)

from athena.knowledge.acquisition.runtime.knowledge_runtime_factory import (
    KnowledgeRuntimeFactory,
)

from athena.knowledge.repositories.sqlite_knowledge_repository import (
    SQLiteKnowledgeRepository,
)

from athena.knowledge.repositories.sqlite_evidence_repository import (
    SQLiteEvidenceRepository,
)

from athena.knowledge.repositories.sqlite_citation_repository import (
    SQLiteCitationRepository,
)

from athena.knowledge.services.evidence_build_service import (
    EvidenceBuildService,
)

from athena.knowledge.services.citation_build_service import (
    CitationBuildService,
)

from athena.knowledge.acquisition.services.provider_manager import (
    ProviderManager,
)

from athena.knowledge.acquisition.providers.docling_provider import (
    DoclingProvider,
)

from athena.knowledge.services.knowledge_service import (
    KnowledgeService,
)

from athena.knowledge.services.evidence_service import (
    EvidenceService,
)

from athena.knowledge.services.citation_service import (
    CitationService,
)

from athena.services.knowledge_workspace_service import (
    KnowledgeWorkspaceService,
)

from athena.ai.llm.model_manager import ModelManager


class ApplicationContext:
    """Owns application-wide services."""

    def __init__(self) -> None:
        """Initialize application services."""

        self.workspace_actions = WorkspaceActions()

        #
        # Workspace services
        #

        self.workspace_service = WorkspaceService()

        self.current_workspace: Workspace | None = None

        #
        # Document services
        #

        self.indexing_service: IndexingService | None = None

        self.indexed_document_service: (
            IndexedDocumentService | None
        ) = None

        self.document_service: (
            WorkspaceDocumentService | None
        ) = None

        self.document_viewer_service = (
            DocumentViewerService()
        )

        #
        # Search / organization services
        #

        self.search_service: SearchService | None = None

        self.bookmark_service: BookmarkService | None = None

        self.note_service: NoteService | None = None

        #
        # Knowledge services
        #
        # Created after workspace database initialization
        #

        self.knowledge_service: (
            KnowledgeService | None
        ) = None

        self.knowledge_workspace_service: (
            KnowledgeWorkspaceService | None
        ) = None

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

        self.model_manager: ModelManager | None = None

        self.execution_service: (
            ExecutionService | None
        ) = None

        self.knowledge_compiler = None

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
        # Knowledge runtime
        #

        knowledge_db = (
            athena_directory / "knowledge.db"
        )

        #
        # Knowledge Runtime
        #

        provider_manager = ProviderManager()

        provider_manager.register(
            DoclingProvider()
        )


        #
        # Persistence repositories
        #

        knowledge_repository = (
            SQLiteKnowledgeRepository(
                str(knowledge_db)
            )
        )

        evidence_repository = (
            SQLiteEvidenceRepository(
                str(knowledge_db)
            )
        )

        citation_repository = (
            SQLiteCitationRepository(
                str(knowledge_db)
            )
        )


        #
        # Knowledge application services
        #

        self.knowledge_service = (
            KnowledgeService(
                knowledge_repository
            )
        )

        evidence_service = (
            EvidenceService(
                evidence_repository
            )
        )

        citation_service = (
            CitationService(
                citation_repository
            )
        )


        #
        # Knowledge Workspace API
        #

        self.knowledge_workspace_service = (
            KnowledgeWorkspaceService(
                self.knowledge_service,
                evidence_service=evidence_service,
                citation_service=citation_service,
            )
        )


        #
        # Knowledge compilation services
        #

        citation_builder = (
            CitationBuildService(
                citation_repository
            )
        )

        evidence_builder = (
            EvidenceBuildService(
                evidence_repository
            )
        )


        #
        # Knowledge execution context
        #

        knowledge_context = (
            KnowledgeRuntimeFactory(
                provider_manager=provider_manager,
                knowledge_repository=knowledge_repository,
                evidence_repository=evidence_repository,
                citation_repository=citation_repository,
                evidence_build_service=evidence_builder,
                citation_build_service=citation_builder,
            )
            .create_context()
        )


        #
        # Document → Knowledge compilation
        #

        knowledge_compiler = (
            KnowledgeCompilationService(
                context=knowledge_context,
            )
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
            knowledge_compiler=knowledge_compiler,
            knowledge_context=knowledge_context,
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

        self.model_manager = (
            self.llm_runtime_bootstrap.initialize()
        )

        self.runtime_router = RuntimeRouter(
            model_manager=self.model_manager,
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

        if (
            self.current_workspace is not None
            and self.conversation_service is not None
        ):
            self.conversation_service.save(
                self.current_workspace.path
                / ".athena"
                / "conversation.json",
            )

        #
        # Document services
        #

        self.document_service = None

        self.indexing_service = None

        self.indexed_document_service = None

        self.search_service = None

        #
        # Knowledge services
        #

        self.knowledge_service = None

        self.knowledge_workspace_service = None

        #
        # User data services
        #

        self.bookmark_service = None

        self.note_service = None

        #
        # AI services
        #

        self.rag_service = None

        self.retrieval_service = None

        self.metadata_service = None

        self.athena_query_service = None

        self.conversation_query_service = None

        #
        # Settings
        #

        self.ai_settings_service = None

        self.llm_settings = None

        #
        # Conversation services
        #

        self.conversation_execution_service = None

        self.conversation_service = None

        #
        # Runtime services
        #

        self.llm_runtime_bootstrap = None

        self.runtime_router = None

        self.execution_service = None

        #
        # Workspace
        #

        self.current_workspace = None

    def get_provider_health(self):
        """Return AI provider health information."""

        if self.runtime_router is None:
            return []

        return self.runtime_router.get_provider_health()


    @property
    def workspace(self) -> Workspace:
        """Return the currently open workspace."""

        if self.current_workspace is None:
            raise RuntimeError(
                "No workspace is currently open.",
            )

        return self.current_workspace

