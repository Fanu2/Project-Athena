"""
Tests for assistant recovery service.
"""

from athena.application.assistant.in_memory_session_store import (
    InMemoryAssistantSessionStore,
)

from athena.application.assistant.recovery_service import (
    AssistantRecoveryService,
)

from athena.application.assistant.session import (
    create_assistant_session,
)


def test_recovery_restores_session():

    store = InMemoryAssistantSessionStore()

    session = create_assistant_session(
        workspace_id="workspace-001",
        workspace_name="Research",
        conversation_id="conv-001",
    )

    store.save(
        session,
    )

    recovery = AssistantRecoveryService(
        store,
    )

    restored = recovery.restore(
        session.session_id,
    )

    assert restored == session


def test_recovery_lists_sessions():

    store = InMemoryAssistantSessionStore()

    session = create_assistant_session(
        workspace_id="workspace-001",
        workspace_name="Research",
        conversation_id="conv-001",
    )

    store.save(
        session,
    )

    recovery = AssistantRecoveryService(
        store,
    )

    sessions = recovery.available_sessions()

    assert len(sessions) == 1
