"""
Tests for context window manager.
"""

from __future__ import annotations

from athena.ai.llm.context_window_manager import (
    ContextWindowManager,
)
from athena.ai.llm.conversation_context import (
    ConversationContext,
)


def test_trim_recent_messages() -> None:
    context = ConversationContext(
        conversation_id="test",
        recent_messages=[
            "one",
            "two",
            "three",
            "four",
        ],
    )

    result = ContextWindowManager(
        max_messages=2,
    ).optimize(
        context
    )

    assert result.recent_messages == [
        "three",
        "four",
    ]


def test_limit_retrieved_knowledge() -> None:
    context = ConversationContext(
        conversation_id="test",
        retrieved_knowledge=[
            "a",
            "b",
            "c",
            "d",
        ],
    )

    result = ContextWindowManager(
        max_knowledge_items=2,
    ).optimize(
        context
    )

    assert result.retrieved_knowledge == [
        "a",
        "b",
    ]


def test_preserve_summary() -> None:
    context = ConversationContext(
        conversation_id="test",
        summary="Athena summary",
    )

    result = ContextWindowManager().optimize(
        context
    )

    assert result.summary == (
        "Athena summary"
    )
