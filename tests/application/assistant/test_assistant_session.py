"""
Tests for assistant session model.
"""

from athena.application.assistant.session import (
    create_assistant_session,
)


def test_assistant_session_creation():

    session = create_assistant_session(
        workspace_name="Research",
        workspace_id="workspace-001",
        conversation_id="conv-001",
    )

    assert (
        session.workspace_name
        == "Research"
    )

    assert (
        session.conversation_id
        == "conv-001"
    )

    assert session.session_id
