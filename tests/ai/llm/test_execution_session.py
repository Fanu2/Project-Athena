"""
Tests for session based execution.
"""

from __future__ import annotations

from unittest.mock import Mock

from athena.ai.llm.execution_service import ExecutionService
from athena.ai.llm.model_info import ModelInfo
from athena.ai.llm.models import LLMResponse
from athena.ai.llm.runtime_request import RuntimeRequest
from athena.ai.llm.session import LLMSession


def test_execute_session_builds_request() -> None:
    router = Mock()

    router.route.return_value = ModelInfo(
        name="qwen3:4b",
        provider="ollama",
    )

    provider = Mock()

    provider.analyze.return_value = LLMResponse(
        text="response",
        model="qwen3:4b",
    )

    factory = Mock()
    factory.create.return_value = provider

    service = ExecutionService(
        router=router,
        factory=factory,
    )

    session = LLMSession(
        model="qwen3:4b",
        system_prompt="You are Athena.",
    )

    response = service.execute_session(
        RuntimeRequest(),
        session,
        "Explain RAG",
    )

    assert response.text == "response"

    provider.analyze.assert_called_once()

    request = provider.analyze.call_args.args[0]

    assert request.system_prompt == (
        "You are Athena."
    )

    assert request.user_prompt == (
        "Explain RAG"
    )

    assert request.model_name == (
        "qwen3:4b"
    )
