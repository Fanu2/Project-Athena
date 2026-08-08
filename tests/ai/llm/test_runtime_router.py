"""
Tests for RuntimeRouter.
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from athena.ai.llm.capabilities import ModelCapabilities
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

    manager = ModelManager(
        provider_registry=providers,
    )

    manager.register_model(
        ModelInfo(
            name="qwen3:4b",
            provider="ollama",
            capabilities=ModelCapabilities(
                chat=True,
            ),
        )
    )

    manager.register_model(
        ModelInfo(
            name="llava",
            provider="ollama",
            capabilities=ModelCapabilities(
                vision=True,
            ),
        )
    )

    manager.register_model(
        ModelInfo(
            name="nomic-embed-text",
            provider="ollama",
            capabilities=ModelCapabilities(
                embeddings=True,
            ),
        )
    )

    return manager


def test_route_preferred_model() -> None:
    router = RuntimeRouter(
        create_manager()
    )

    result = router.route(
        RuntimeRequest(
            preferred_model="llava",
            capability="vision",
        )
    )

    assert result.name == "llava"


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


def test_route_finds_capable_fallback_model() -> None:
    router = RuntimeRouter(
        create_manager()
    )

    result = router.route(
        RuntimeRequest(
            capability="vision",
        )
    )

    assert result.name == "llava"


def test_route_finds_embedding_model() -> None:
    router = RuntimeRouter(
        create_manager()
    )

    result = router.route(
        RuntimeRequest(
            capability="embedding",
        )
    )

    assert result.name == "nomic-embed-text"