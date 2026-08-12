from athena.application.assistant.workspace_context import (
    AssistantWorkspaceContext,
)


def test_workspace_context_contains_workspace_state():
    context = AssistantWorkspaceContext(
        workspace_name="Research",
        document_count=10,
        knowledge_item_count=5,
        conversation_messages=20,
        recent_documents=(
            "report.pdf",
            "notes.md",
        ),
        recent_queries=(
            "Find ownership details",
        ),
        recent_sessions=(
            "session-001",
        ),
    )

    assert context.workspace_name == "Research"

    assert context.document_count == 10

    assert context.knowledge_item_count == 5

    assert context.conversation_messages == 20

    assert context.recent_documents == (
        "report.pdf",
        "notes.md",
    )

    assert context.recent_queries == (
        "Find ownership details",
    )

    assert context.recent_sessions == (
        "session-001",
    )
