"""
Tests for ModelRegistry.
"""

from __future__ import annotations

import pytest

from athena.ai.llm.model_info import ModelInfo
from athena.ai.llm.model_registry import ModelRegistry


def test_register_model() -> None:
    registry = ModelRegistry()

    model = ModelInfo(
        name="qwen3:4b",
        provider="ollama",
    )

    registry.register(model)

    assert registry.exists("qwen3:4b")
    assert registry.get("qwen3:4b") == model


def test_duplicate_model_registration() -> None:
    registry = ModelRegistry()

    model = ModelInfo(
        name="qwen3:4b",
        provider="ollama",
    )

    registry.register(model)

    with pytest.raises(ValueError):
        registry.register(model)


def test_models_by_provider() -> None:
    registry = ModelRegistry()

    registry.register(
        ModelInfo(
            name="qwen3:4b",
            provider="ollama",
        )
    )

    registry.register(
        ModelInfo(
            name="gpt-5",
            provider="openai",
        )
    )

    models = registry.by_provider("ollama")

    assert len(models) == 1
    assert models[0].name == "qwen3:4b"


def test_active_model() -> None:
    registry = ModelRegistry()

    registry.register(
        ModelInfo(
            name="qwen3:4b",
            provider="ollama",
        )
    )

    registry.register(
        ModelInfo(
            name="gpt-5",
            provider="openai",
        )
    )

    registry.set_active("gpt-5")

    assert registry.active().name == "gpt-5"


def test_missing_active_model() -> None:
    registry = ModelRegistry()

    with pytest.raises(RuntimeError):
        registry.active()
