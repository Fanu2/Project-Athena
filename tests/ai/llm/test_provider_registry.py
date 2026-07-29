"""
Tests for ProviderRegistry.
"""

from __future__ import annotations

import pytest

from athena.ai.llm import (
    LLMProvider,
    ProviderRegistry,
)
from athena.ai.llm.models import (
    LLMRequest,
    LLMResponse,
)


class FakeProvider(LLMProvider):
    @property
    def provider_name(self) -> str:
        return "fake"

    def analyze(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        return LLMResponse(
            text="ok",
            model="fake",
        )


def test_register_provider() -> None:
    registry = ProviderRegistry()
    provider = FakeProvider()

    registry.register(provider)

    assert registry.exists("fake")
    assert registry.get("fake") is provider


def test_duplicate_provider_raises() -> None:
    registry = ProviderRegistry()

    registry.register(FakeProvider())

    with pytest.raises(ValueError):
        registry.register(FakeProvider())


def test_default_provider() -> None:
    registry = ProviderRegistry()
    provider = FakeProvider()

    registry.register(provider)

    assert registry.default() is provider


def test_set_default_unknown_provider() -> None:
    registry = ProviderRegistry()

    with pytest.raises(KeyError):
        registry.set_default("missing")


def test_unregister_provider() -> None:
    registry = ProviderRegistry()
    provider = FakeProvider()

    registry.register(provider)
    registry.unregister("fake")

    assert not registry.exists("fake")


def test_names() -> None:
    registry = ProviderRegistry()

    registry.register(FakeProvider())

    assert registry.names() == ["fake"]


def test_providers() -> None:
    registry = ProviderRegistry()
    provider = FakeProvider()

    registry.register(provider)

    assert registry.providers() == [provider]


def test_default_cleared_after_unregister() -> None:
    registry = ProviderRegistry()
    provider = FakeProvider()

    registry.register(provider)
    registry.unregister("fake")

    with pytest.raises(RuntimeError):
        registry.default()

class FakeProvider2(LLMProvider):
    @property
    def provider_name(self) -> str:
        return "fake2"

    def analyze(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        return LLMResponse(
            text="provider2",
            model="fake2",
        )


def test_switch_default_provider() -> None:
    registry = ProviderRegistry()

    p1 = FakeProvider()
    p2 = FakeProvider2()

    registry.register(p1)
    registry.register(p2)

    assert registry.default() is p1

    registry.set_default("fake2")

    assert registry.default() is p2


def test_unregister_default_selects_remaining_provider() -> None:
    registry = ProviderRegistry()

    p1 = FakeProvider()
    p2 = FakeProvider2()

    registry.register(p1)
    registry.register(p2)

    registry.unregister("fake")

    assert registry.default() is p2

def test_provider_default_capabilities() -> None:
    provider = FakeProvider()

    assert provider.capabilities() == {
        "chat": True,
        "vision": False,
        "embedding": False,
        "streaming": False,
        "tools": False,
    }


def test_provider_default_model_list() -> None:
    provider = FakeProvider()

    assert provider.list_models() == []


def test_provider_default_health() -> None:
    provider = FakeProvider()

    assert provider.health() is True
