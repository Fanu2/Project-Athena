"""
Tests for assistant session context.
"""

from athena.application.assistant.context import (
    AssistantContext,
)

from athena.application.assistant.session import (
    create_assistant_session,
)

from athena.ai.intent.models import (
    IntentResult,
)

from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)


def test_context_contains_assistant_session():

    session = create_assistant_session(
        workspace_name="Research",
        conversation_id="conv-001",
    )

    context = AssistantContext(
        intent=IntentResult(
            intent="summary",
            confidence=1.0,
        ),
        workspace=WorkspaceIntelligenceSnapshot(
            workspace_id="workspace-001",
            workspace_name="Research",
            document_count=10,
            knowledge_item_count=5,
            conversation_messages=2,
        ),
        session=session,
    )

    assert (
        context.session
        == session
    )

    assert (
        context.session.conversation_id
        == "conv-001"
    )
