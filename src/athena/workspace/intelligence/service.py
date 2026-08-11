"""
Athena Workspace Intelligence service.

Combines existing workspace services into
a workspace intelligence snapshot.
"""

from __future__ import annotations

from athena.conversation.service import ConversationService

from athena.knowledge.services.evidence_service import (
    EvidenceService,
)

from athena.knowledge.services.citation_service import (
    CitationService,
)

from athena.services.knowledge_workspace_service import (
    KnowledgeWorkspaceService,
)

from athena.services.workspace_query_service import (
    WorkspaceQueryService,
)

from athena.workspace.models import Workspace

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
    ) -> None:
        """
        Initialize workspace intelligence service.
        """

        self._workspace_query = (
            workspace_query_service
        )

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
            knowledge_item_count=knowledge_count,
            evidence_count=evidence_count,
            citation_count=citation_count,
            conversation_id=conversation_id,
            conversation_messages=conversation_messages,
        )
