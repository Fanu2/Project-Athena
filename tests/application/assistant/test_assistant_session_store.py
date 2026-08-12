"""
Tests for assistant session storage.
"""

from athena.application.assistant.in_memory_session_store import (
    InMemoryAssistantSessionStore,
)

from athena.application.assistant.session import (
    create_assistant_session,
)


def test_session_store_save_and_load():

    store = InMemoryAssistantSessionStore()

    session = create_assistant_session(
        workspace_name="Research",
        conversation_id="conv-001",
    )

    store.save(
        session,
    )

    loaded = store.get(
        session.session_id,
    )

    assert loaded == session
