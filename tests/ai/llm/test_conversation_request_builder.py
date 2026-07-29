"""
Tests for conversation request builder.
"""

from __future__ import annotations

from athena.ai.llm.conversation_context import (
    ConversationContext,
)
from athena.ai.llm.conversation_request_builder import (
    ConversationRequestBuilder,
)


def test_build_request_with_context() -> None:
    context = ConversationContext(
        conversation_id="test",
        summary="Athena summary",
        retrieved_knowledge=[
            "RAG knowledge",
        ],
    )

    request = (
        ConversationRequestBuilder()
        .build(
            context,
            "Explain this",
            "qwen3:4b",
        )
    )

    assert request.model_name == (
        "qwen3:4b"
    )

    assert "Athena summary" in (
        request.user_prompt
    )

    assert "RAG knowledge" in (
        request.user_prompt
    )

    assert "Explain this" in (
        request.user_prompt
    )


def test_build_request_empty_context() -> None:
    context = ConversationContext(
        conversation_id="test",
    )

    request = (
        ConversationRequestBuilder()
        .build(
            context,
            "Hello",
            "gemma3:4b",
        )
    )

    assert request.user_prompt == (
        "User request:\nHello"
    )
