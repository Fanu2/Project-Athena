from athena.application.assistant.workspace_context import (
    AssistantWorkspaceContext,
)


def test_workspace_context_contains_workspace_state():

    context = AssistantWorkspaceContext(
        workspace_name="Research",
        document_count=10,
        knowledge_item_count=5,
        conversation_messages=20,
    )

    assert context.workspace_name == "Research"
    assert context.document_count == 10
