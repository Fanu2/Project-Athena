"""
Tests for RuntimeRouter.
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from athena.ai.llm.model_info import ModelInfo
from athena.ai.llm.model_manager import ModelManager
from athena.ai.llm.provider_registry import ProviderRegistry
from athena.ai.llm.runtime_request import RuntimeRequest
from athena.ai.llm.runtime_router import RuntimeRouter


def create_provider(
    name: str,
    vision: bool = False,
) -> Mock:
    provider = Mock()

    provider.provider_name = name

    provider.metadata = Mock(
        name=name,
        display_name=name.title(),
        local=True,
        requires_api_key=False,
        supports_chat=True,
        supports_streaming=False,
        supports_tools=False,
        supports_vision=vision,
    )

    return provider


def create_manager() -> ModelManager:
    providers = ProviderRegistry()

    providers.register(
        create_provider("ollama")
    )

    providers.register(
        create_provider(
            "openai",
            vision=True,
        )
    )

    manager = ModelManager(
        provider_registry=providers,
    )

    manager.register_model(
        ModelInfo(
            name="qwen3:4b",
            provider="ollama",
        )
    )

    manager.register_model(
        ModelInfo(
            name="gpt-5",
            provider="openai",
        )
    )

    return manager


def test_route_preferred_model() -> None:
    router = RuntimeRouter(
        create_manager()
    )

    result = router.route(
        RuntimeRequest(
            preferred_model="gpt-5",
        )
    )

    assert result.name == "gpt-5"


def test_route_active_model_fallback() -> None:
    router = RuntimeRouter(
        create_manager()
    )

    result = router.route(
        RuntimeRequest()
    )

    assert result.name == "qwen3:4b"


def test_route_missing_model_without_fallback() -> None:
    router = RuntimeRouter(
        create_manager()
    )

    with pytest.raises(ValueError):
        router.route(
            RuntimeRequest(
                preferred_model="missing-model",
                allow_fallback=False,
            )
        )


def test_route_rejects_unsupported_capability() -> None:
    router = RuntimeRouter(
        create_manager()
    )

    with pytest.raises(ValueError):
        router.route(
            RuntimeRequest(
                preferred_model="qwen3:4b",
                capability="vision",
            )
        )
