"""
Tests for assistant session storage.
"""

from athena.application.assistant.in_memory_session_store import (
    InMemoryAssistantSessionStore,
)

from athena.application.assistant.session import (
    create_assistant_session,
)


def create_test_session():
    return create_assistant_session(
        workspace_id="workspace-001",
        workspace_name="Research",
        conversation_id="conv-001",
    )


def test_session_store_save_and_load():

    store = InMemoryAssistantSessionStore()

    session = create_test_session()

    store.save(
        session,
    )

    loaded = store.get(
        session.session_id,
    )

    assert loaded == session


def test_session_store_lists_sessions():

    store = InMemoryAssistantSessionStore()

    session = create_test_session()

    store.save(
        session,
    )

    sessions = store.list_sessions()

    assert len(sessions) == 1

    assert (
        sessions[0]
        == session
    )


def test_session_store_deletes_session():

    store = InMemoryAssistantSessionStore()

    session = create_test_session()

    store.save(
        session,
    )

    store.delete(
        session.session_id,
    )

    assert (
        store.get(
            session.session_id,
        )
        is None
    )
