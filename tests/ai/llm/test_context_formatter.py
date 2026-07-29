"""
Tests for context formatter.
"""

from __future__ import annotations

from athena.ai.llm.context_formatter import (
    ContextFormatter,
)
from athena.ai.llm.conversation_context import (
    ConversationContext,
)


def test_format_full_context() -> None:
    context = ConversationContext(
        conversation_id="test",
        summary="Athena discussion",
        recent_messages=[
            "Explain RAG",
        ],
        retrieved_knowledge=[
            "RAG uses retrieval",
        ],
    )

    result = ContextFormatter().format(
        context,
        "How does it work?",
    )

    assert "Athena discussion" in result
    assert "Explain RAG" in result
    assert "RAG uses retrieval" in result
    assert "How does it work?" in result


def test_format_empty_context() -> None:
    context = ConversationContext(
        conversation_id="test",
    )

    result = ContextFormatter().format(
        context,
        "Hello",
    )

    assert result == (
        "User request:\nHello"
    )


def test_format_without_knowledge() -> None:
    context = ConversationContext(
        conversation_id="test",
        summary="Summary",
    )

    result = ContextFormatter().format(
        context,
        "Question",
    )

    assert "Summary" in result
    assert "Question" in result
