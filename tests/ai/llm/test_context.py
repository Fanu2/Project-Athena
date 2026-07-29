"""
Tests for LLM context builder.
"""

from __future__ import annotations

from athena.ai.llm.context import (
    ContextBuilder,
    LLMContext,
)
from athena.ai.llm.message import Message
from athena.ai.llm.session import LLMSession


def test_build_context_from_session() -> None:
    session = LLMSession(
        model="qwen3:4b",
        system_prompt="You are Athena.",
    )

    session.add_message(
        Message(
            role="user",
            content="Hello",
        )
    )

    builder = ContextBuilder()

    context = builder.build(
        session
    )

    assert isinstance(
        context,
        LLMContext,
    )

    assert context.system_prompt == (
        "You are Athena."
    )

    assert len(
        context.messages
    ) == 1


def test_context_preserves_message_order() -> None:
    session = LLMSession()

    session.add_message(
        Message(
            role="user",
            content="Question",
        )
    )

    session.add_message(
        Message(
            role="assistant",
            content="Answer",
        )
    )

    context = ContextBuilder().build(
        session
    )

    assert context.messages[0].role == "user"
    assert context.messages[1].role == "assistant"


def test_build_request_from_session() -> None:
    session = LLMSession(
        model="qwen3:4b",
        system_prompt="You are Athena.",
    )

    request = ContextBuilder().build_request(
        session,
        "Explain RAG.",
    )

    assert request.system_prompt == (
        "You are Athena."
    )

    assert request.user_prompt == (
        "Explain RAG."
    )

    assert request.model_name == (
        "qwen3:4b"
    )
