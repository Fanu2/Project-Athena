"""
Tests for ModelValidator.
"""

from __future__ import annotations

from athena.ai.llm.metadata import ProviderMetadata
from athena.ai.llm.model_info import ModelInfo
from athena.ai.llm.model_validator import ModelValidator


def test_chat_capability() -> None:
    validator = ModelValidator()

    model = ModelInfo(
        name="qwen3:4b",
        provider="ollama",
    )

    metadata = ProviderMetadata(
        name="ollama",
        display_name="Ollama",
        local=True,
        requires_api_key=False,
        supports_chat=True,
        supports_streaming=False,
        supports_tools=False,
        supports_vision=False,
    )

    assert validator.validate_capability(
        model,
        metadata,
        "chat",
    ) is True


def test_vision_not_supported() -> None:
    validator = ModelValidator()

    model = ModelInfo(
        name="qwen3:4b",
        provider="ollama",
    )

    metadata = ProviderMetadata(
        name="ollama",
        display_name="Ollama",
        local=True,
        requires_api_key=False,
        supports_chat=True,
        supports_streaming=False,
        supports_tools=False,
        supports_vision=False,
    )

    assert validator.validate_capability(
        model,
        metadata,
        "vision",
    ) is False


def test_unknown_capability() -> None:
    validator = ModelValidator()

    model = ModelInfo(
        name="gpt-5",
        provider="openai",
    )

    metadata = ProviderMetadata(
        name="openai",
        display_name="OpenAI",
        local=False,
        requires_api_key=True,
        supports_chat=True,
        supports_streaming=True,
        supports_tools=True,
        supports_vision=True,
    )

    try:
        validator.validate_capability(
            model,
            metadata,
            "unknown",
        )
    except ValueError:
        assert True
    else:
        assert False
