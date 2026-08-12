"""
Tests assistant context session integration.
"""

from athena.application.assistant.context import (
    AssistantContext,
)

from athena.application.assistant.session import (
    create_assistant_session,
)

from athena.ai.intent.models import (
    IntentResult,
    IntentType,
)

from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)


def test_context_contains_assistant_session():

    session = create_assistant_session(
        workspace_id="workspace-001",
        workspace_name="Research",
        conversation_id="conv-001",
    )

    workspace = WorkspaceIntelligenceSnapshot(
        workspace_id="workspace-001",
        workspace_name="Research",
        document_count=10,
        knowledge_item_count=5,
        conversation_messages=2,
    )

    intent = IntentResult(
        intent=IntentType.SEARCH,
        confidence=1.0,
    )

    context = AssistantContext(
        intent=intent,
        workspace=workspace,
    )

    assert (
        context.workspace.workspace_id
        == session.workspace_id
    )

    assert (
        session.workspace_name
        == "Research"
    )

    assert (
        session.conversation_id
        == "conv-001"
    )
