"""
Tests for ModelManager.
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from athena.ai.llm.model_info import ModelInfo
from athena.ai.llm.model_manager import ModelManager
from athena.ai.llm.provider_registry import ProviderRegistry


def test_register_model() -> None:
    manager = ModelManager()

    model = ModelInfo(
        name="qwen3:4b",
        provider="ollama",
    )

    manager.register_model(model)

    assert manager.get_model("qwen3:4b") == model


def test_active_model_switch() -> None:
    manager = ModelManager()

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

    manager.set_active_model("gpt-5")

    assert manager.active_model().name == "gpt-5"


def test_models_listing() -> None:
    manager = ModelManager()

    manager.register_model(
        ModelInfo(
            name="qwen3:4b",
            provider="ollama",
        )
    )

    assert len(manager.models()) == 1


def test_discover_provider_models() -> None:
    provider_registry = ProviderRegistry()

    provider = Mock()
    provider.provider_name = "ollama"
    provider.list_models.return_value = [
        "qwen3:4b",
        "llama3",
    ]

    provider_registry.register(provider)

    manager = ModelManager(
        provider_registry=provider_registry,
    )

    models = manager.discover_provider_models("ollama")

    assert len(models) == 2
    assert models[0].provider == "ollama"


def test_discover_all_models() -> None:
    provider_registry = ProviderRegistry()

    ollama = Mock()
    ollama.provider_name = "ollama"
    ollama.list_models.return_value = [
        "qwen3:4b",
    ]

    openai = Mock()
    openai.provider_name = "openai"
    openai.list_models.return_value = [
        "gpt-5",
    ]

    provider_registry.register(ollama)
    provider_registry.register(openai)

    manager = ModelManager(
        provider_registry=provider_registry,
    )

    models = manager.discover_all_models()

    assert len(models) == 2
    assert models[0].provider in [
        "ollama",
        "openai",
    ]


def test_missing_provider_discovery() -> None:
    manager = ModelManager()

    with pytest.raises(KeyError):
        manager.discover_provider_models("unknown")
