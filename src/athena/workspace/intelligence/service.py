"""
Athena Workspace Intelligence service.

Combines existing workspace services into
a workspace intelligence snapshot.
"""

from __future__ import annotations

from athena.conversation.service import ConversationService
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
    ) -> None:

        self._workspace_query = (
            workspace_query_service
        )

        self._knowledge_workspace = (
            knowledge_workspace_service
        )

        self._conversation = (
            conversation_service
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
            conversation_id=conversation_id,
            conversation_messages=conversation_messages,
        )
