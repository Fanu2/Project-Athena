"""
Athena Workspace Intelligence service.

Combines existing workspace services into
a workspace intelligence snapshot.
"""

from __future__ import annotations

from athena.application.assistant.session_store import (
    AssistantSessionStore,
)

from athena.conversation.models import (
    MessageRole,
)

from athena.conversation.service import (
    ConversationService,
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

from athena.services.workspace_document_service import (
    WorkspaceDocumentService,
)

from athena.services.workspace_query_service import (
    WorkspaceQueryService,
)

from athena.workspace.models import (
    Workspace,
)

from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)


class WorkspaceIntelligenceService:
    """
    Provides workspace intelligence views.

    This service does not own data.
    It aggregates existing Athena services.
    """

    def __init__(
        self,
        workspace_query_service: WorkspaceQueryService,
        knowledge_workspace_service: KnowledgeWorkspaceService | None = None,
        conversation_service: ConversationService | None = None,
        evidence_service: EvidenceService | None = None,
        citation_service: CitationService | None = None,
        document_service: WorkspaceDocumentService | None = None,
        session_store: AssistantSessionStore | None = None,
    ) -> None:
        """
        Initialize workspace intelligence service.
        """

        self._workspace_query = workspace_query_service

        self._knowledge_workspace = (
            knowledge_workspace_service
        )

        self._conversation = (
            conversation_service
        )

        self._evidence = (
            evidence_service
        )

        self._citations = (
            citation_service
        )

        self._documents = (
            document_service
        )

        self._session_store = (
            session_store
        )

    def _recent_documents(
        self,
    ) -> tuple[str, ...]:
        """
        Return recent workspace documents.

        A20.4.1.1:
        Exposes document activity context
        through workspace intelligence.
        """

        if self._documents is None:
            return ()

        documents = (
            self._documents.list_documents()
        )

        return tuple(
            document.name
            for document in documents[-5:]
        )

    def _recent_queries(
        self,
    ) -> tuple[str, ...]:
        """
        Return recent user queries.

        A20.4.1.2:
        Exposes conversation activity context
        through workspace intelligence.
        """

        if self._conversation is None:
            return ()

        messages = (
            self._conversation.conversation.messages
        )

        queries = [
            message.text
            for message in messages
            if message.role == MessageRole.USER
        ]

        return tuple(
            queries[-5:]
        )

    def _recent_sessions(
        self,
        workspace: Workspace,
    ) -> tuple[str, ...]:
        """
        Return recent assistant sessions
        for the workspace.

        A20.4.1.3:
        Exposes assistant continuity
        through workspace intelligence.
        """

        if self._session_store is None:
            return ()

        sessions = [
            session.session_id
            for session in self._session_store.list_sessions()
            if session.workspace_id
            == str(workspace.workspace_id)
        ]

        return tuple(
            sessions[-5:]
        )

    def snapshot(
        self,
        workspace: Workspace,
    ) -> WorkspaceIntelligenceSnapshot:
        """
        Build current workspace intelligence snapshot.
        """

        library = (
            self._workspace_query.library_summary()
        )

        knowledge_count = 0

        if self._knowledge_workspace is not None:
            knowledge_count = len(
                self._knowledge_workspace.list_workspace_items()
            )

        evidence_count = 0

        if self._evidence is not None:
            evidence_count = len(
                self._evidence.list_evidence()
            )

        citation_count = 0

        if self._citations is not None:
            citation_count = len(
                self._citations.list_citations()
            )

        conversation_id = None
        conversation_messages = 0

        if self._conversation is not None:
            conversation = (
                self._conversation.conversation
            )

            conversation_id = (
                conversation.conversation_id
            )

            conversation_messages = len(
                conversation.messages
            )

        return WorkspaceIntelligenceSnapshot(
            workspace_id=workspace.workspace_id,

            workspace_name=workspace.name,

            document_count=library.get(
                "documents",
                0,
            ),

            page_count=library.get(
                "pages",
                0,
            ),

            indexed_document_count=library.get(
                "documents",
                0,
            ),

            knowledge_item_count=knowledge_count,

            evidence_count=evidence_count,

            citation_count=citation_count,

            conversation_id=conversation_id,

            conversation_messages=conversation_messages,

            active_document=None,

            #
            # A20.4 Workspace Intelligence Context
            #

            recent_documents=(
                self._recent_documents()
            ),

            recent_queries=(
                self._recent_queries()
            ),

            recent_sessions=(
                self._recent_sessions(
                    workspace,
                )
            ),
        )
