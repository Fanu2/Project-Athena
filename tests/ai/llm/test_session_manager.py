"""
Tests for SessionManager.
"""

from __future__ import annotations

import pytest

from athena.ai.llm.message import Message
from athena.ai.llm.session_manager import SessionManager


def test_create_session() -> None:
    manager = SessionManager()

    session = manager.create(
        model="qwen3:4b",
        system_prompt="You are Athena.",
    )

    assert manager.exists(
        session.session_id
    )

    assert session.model == "qwen3:4b"


def test_session_message_history() -> None:
    manager = SessionManager()

    session = manager.create()

    session.add_message(
        Message(
            role="user",
            content="Hello",
        )
    )

    history = session.history()

    assert len(history) == 1
    assert history[0].content == "Hello"


def test_list_sessions() -> None:
    manager = SessionManager()

    manager.create()
    manager.create()

    assert len(manager.sessions()) == 2


def test_remove_session() -> None:
    manager = SessionManager()

    session = manager.create()

    manager.remove(
        session.session_id
    )

    assert not manager.exists(
        session.session_id
    )


def test_missing_session() -> None:
    manager = SessionManager()

    with pytest.raises(KeyError):
        manager.get(
            "missing-session"
        )
