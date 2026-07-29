"""
Tests for conversation execution service.
"""

from __future__ import annotations

from unittest.mock import Mock

from athena.ai.llm.conversation import Conversation
from athena.ai.llm.conversation_execution_service import (
    ConversationExecutionService,
)
from athena.ai.llm.models import (
    LLMResponse,
)
from athena.ai.llm.runtime_request import (
    RuntimeRequest,
)


def test_execute_conversation_request() -> None:
    executor = Mock()

    executor.execute.return_value = (
        LLMResponse(
            text="Athena answer",
            model="qwen3:4b",
        )
    )

    service = ConversationExecutionService(
        executor=executor,
    )

    conversation = Conversation()

    result = service.execute(
        conversation,
        "Explain Athena",
        RuntimeRequest(),
    )

    assert result.response.text == (
        "Athena answer"
    )

    assert result.conversation_id == (
        conversation.conversation_id
    )


def test_execute_uses_execution_service() -> None:
    executor = Mock()

    executor.execute.return_value = (
        LLMResponse(
            text="response",
            model="gemma3:4b",
        )
    )

    service = ConversationExecutionService(
        executor=executor,
    )

    service.execute(
        Conversation(),
        "hello",
        RuntimeRequest(),
    )

    assert executor.execute.called


def test_execute_preserves_response_model() -> None:
    executor = Mock()

    executor.execute.return_value = (
        LLMResponse(
            text="ok",
            model="qwen3:4b",
        )
    )

    result = ConversationExecutionService(
        executor=executor,
    ).execute(
        Conversation(),
        "test",
        RuntimeRequest(),
    )

    assert result.response.model == (
        "qwen3:4b"
    )


def test_execute_persists_assistant_response() -> None:
    executor = Mock()

    executor.execute.return_value = (
        LLMResponse(
            text="Athena response",
            model="qwen3:4b",
        )
    )

    conversation = Conversation()

    ConversationExecutionService(
        executor=executor,
    ).execute(
        conversation,
        "hello",
        RuntimeRequest(),
    )

    history = conversation.history()

    assert len(history) == 1

    assert history[0].role == "assistant"

    assert history[0].content == (
        "Athena response"
    )
