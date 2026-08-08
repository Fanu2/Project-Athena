"""
Tests for ModelManager service.
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from athena.ai.llm.model_info import ModelInfo
from athena.ai.llm.model_manager import ModelManager
from athena.ai.llm.model_registry import ModelRegistry
from athena.ai.llm.provider_registry import ProviderRegistry


def create_manager() -> ModelManager:
    """Create test model manager."""

    return ModelManager(
        model_registry=ModelRegistry(),
        provider_registry=ProviderRegistry(),
    )


def test_register_model() -> None:
    """Register and retrieve model."""

    manager = create_manager()

    model = ModelInfo(
        name="qwen3:4b",
        provider="ollama",
    )

    manager.register_model(model)

    assert manager.has_model("qwen3:4b")
    assert manager.get_model("qwen3:4b") == model


def test_models_by_capability() -> None:
    """Return models matching capability."""

    manager = create_manager()

    manager.register_model(
        ModelInfo(
            name="llava",
            provider="ollama",
        )
    )

    models = manager.models()

    assert len(models) == 1
    assert models[0].name == "llava"


def test_get_chat_profile() -> None:
    """Return chat profile."""

    manager = create_manager()

    profile = manager.get_profile("chat")

    assert profile.model_name == "qwen3:4b"
    assert profile.provider == "ollama"


def test_get_vision_profile() -> None:
    """Return vision profile."""

    manager = create_manager()

    profile = manager.get_profile("vision")

    assert profile.model_name == "llava"


def test_get_embedding_profile() -> None:
    """Return embedding profile."""

    manager = create_manager()

    profile = manager.get_profile("embedding")

    assert profile.model_name == "nomic-embed-text"


def test_missing_profile() -> None:
    """Reject unknown capability profile."""

    manager = create_manager()

    with pytest.raises(ValueError):
        manager.get_profile("unknown")