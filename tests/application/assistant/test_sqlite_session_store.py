"""
Tests for SQLite assistant session store.
"""

from pathlib import Path

from athena.application.assistant.sqlite_session_store import (
    SQLiteAssistantSessionStore,
)

from athena.application.assistant.session import (
    create_assistant_session,
)


def test_sqlite_session_store_save_and_load(
    tmp_path: Path,
):

    store = SQLiteAssistantSessionStore(
        tmp_path / "assistant.db",
    )

    session = create_assistant_session(
        workspace_id="workspace-001",
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


def test_sqlite_session_store_lists_sessions(
    tmp_path: Path,
):

    store = SQLiteAssistantSessionStore(
        tmp_path / "assistant.db",
    )

    session = create_assistant_session(
        workspace_id="workspace-001",
        workspace_name="Research",
        conversation_id="conv-001",
    )

    store.save(
        session,
    )

    sessions = store.list_sessions()

    assert len(sessions) == 1
