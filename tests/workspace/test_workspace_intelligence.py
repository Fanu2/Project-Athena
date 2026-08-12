"""
Tests for Athena Workspace Intelligence.
"""

from datetime import datetime
from pathlib import Path

from athena.conversation.service import (
    ConversationService,
)

from athena.services.workspace_query_service import (
    WorkspaceQueryService,
)

from athena.workspace.models import (
    Workspace,
)

from athena.workspace.intelligence.service import (
    WorkspaceIntelligenceService,
)


class FakeIndexedDocumentService:
    """
    Minimal document service for workspace intelligence tests.
    """

    def list_documents(
        self,
    ):
        return []


def test_workspace_intelligence_snapshot():
    workspace = Workspace(
        name="Research",
        path=Path("/tmp/research"),
        version="2.0",
        created=datetime.now(),
        modified=datetime.now(),
    )

    query_service = WorkspaceQueryService(
        indexed_document_service=FakeIndexedDocumentService(),
    )

    conversation_service = ConversationService()

    conversation_service.add_user_message(
        "Explain Athena architecture",
    )

    conversation_service.add_assistant_message(
        "Athena uses offline-first architecture",
    )

    conversation_service.add_user_message(
        "Explain session recovery",
    )

    service = WorkspaceIntelligenceService(
        workspace_query_service=query_service,
        conversation_service=conversation_service,
    )

    snapshot = service.snapshot(
        workspace,
    )

    assert (
        snapshot.workspace_id
        == workspace.workspace_id
    )

    assert (
        snapshot.workspace_name
        == "Research"
    )

    assert (
        snapshot.conversation_id
        is not None
    )

    assert (
        snapshot.conversation_messages
        == 3
    )

    assert (
        snapshot.recent_queries
        == (
            "Explain Athena architecture",
            "Explain session recovery",
        )
    )
