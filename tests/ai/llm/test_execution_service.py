"""
Tests for ExecutionService.
"""

from __future__ import annotations

import pytest

from unittest.mock import Mock

from athena.ai.llm.execution_service import ExecutionService
from athena.ai.llm.model_info import ModelInfo
from athena.ai.llm.models import (
    LLMRequest,
    LLMResponse,
)
from athena.ai.llm.runtime_request import RuntimeRequest


def test_execute_routes_and_calls_provider() -> None:
    router = Mock()

    router.route.return_value = ModelInfo(
        name="qwen3:4b",
        provider="ollama",
    )

    provider = Mock()

    provider.analyze.return_value = LLMResponse(
        text="hello",
        model="qwen3:4b",
    )

    factory = Mock()

    factory.create.return_value = provider

    service = ExecutionService(
        router=router,
        factory=factory,
    )

    response = service.execute(
        RuntimeRequest(),
        LLMRequest(
            system_prompt="system",
            user_prompt="hello",
        ),
    )

    assert response.text == "hello"

    router.route.assert_called_once()

    factory.create.assert_called_once_with(
        "ollama"
    )

    provider.analyze.assert_called_once()


def test_execute_uses_selected_provider() -> None:
    router = Mock()

    router.route.return_value = ModelInfo(
        name="gpt-5",
        provider="openai",
    )

    factory = Mock()

    factory.create.return_value = Mock(
        analyze=Mock(
            return_value=LLMResponse(
                text="response",
                model="gpt-5",
            )
        )
    )

    service = ExecutionService(
        router=router,
        factory=factory,
    )

    service.execute(
        RuntimeRequest(
            preferred_model="gpt-5",
        ),
        LLMRequest(
            system_prompt="",
            user_prompt="test",
        ),
    )

    factory.create.assert_called_once_with(
        "openai"
    )

from athena.ai.llm.exceptions import (
    GenerationError,
    ProviderUnavailableError,
)
from athena.ai.llm.execution_error import (
    ExecutionFailedError,
    ExecutionUnavailableError,
)


def test_execute_provider_unavailable() -> None:
    router = Mock()

    router.route.return_value = ModelInfo(
        name="qwen3:4b",
        provider="ollama",
    )

    provider = Mock()

    provider.analyze.side_effect = (
        ProviderUnavailableError(
            "offline"
        )
    )

    factory = Mock()
    factory.create.return_value = provider

    service = ExecutionService(
        router=router,
        factory=factory,
    )

    with pytest.raises(
        ExecutionUnavailableError
    ):
        service.execute(
            RuntimeRequest(),
            LLMRequest(
                system_prompt="",
                user_prompt="test",
            ),
        )


def test_execute_generation_failure() -> None:
    router = Mock()

    router.route.return_value = ModelInfo(
        name="qwen3:4b",
        provider="ollama",
    )

    provider = Mock()

    provider.analyze.side_effect = (
        GenerationError(
            "failed"
        )
    )

    factory = Mock()
    factory.create.return_value = provider

    service = ExecutionService(
        router=router,
        factory=factory,
    )

    with pytest.raises(
        ExecutionFailedError
    ):
        service.execute(
            RuntimeRequest(),
            LLMRequest(
                system_prompt="",
                user_prompt="test",
            ),
        )



