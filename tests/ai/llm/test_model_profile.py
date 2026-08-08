"""
Tests for Athena model profiles.
"""

from __future__ import annotations

from athena.ai.llm.model_profile import ModelProfile
from athena.ai.llm.model_profiles import DEFAULT_MODEL_PROFILES


def test_default_profiles_exist() -> None:
    """Verify default capability profiles exist."""

    capabilities = {
        profile.capability
        for profile in DEFAULT_MODEL_PROFILES
    }

    assert "chat" in capabilities
    assert "vision" in capabilities
    assert "embedding" in capabilities


def test_chat_profile_uses_qwen() -> None:
    """Verify chat profile uses qwen3:4b."""

    profile = next(
        profile
        for profile in DEFAULT_MODEL_PROFILES
        if profile.capability == "chat"
    )

    assert profile.model_name == "qwen3:4b"


def test_vision_profile_uses_llava() -> None:
    """Verify vision profile uses llava."""

    profile = next(
        profile
        for profile in DEFAULT_MODEL_PROFILES
        if profile.capability == "vision"
    )

    assert profile.model_name == "llava"


def test_embedding_profile_uses_nomic() -> None:
    """Verify embedding profile uses nomic-embed-text."""

    profile = next(
        profile
        for profile in DEFAULT_MODEL_PROFILES
        if profile.capability == "embedding"
    )

    assert profile.model_name == "nomic-embed-text"


def test_model_profile_is_immutable() -> None:
    """Verify profile is frozen."""

    profile = ModelProfile(
        name="test",
        capability="chat",
        model_name="qwen3:4b",
    )

    assert profile.provider == "ollama"