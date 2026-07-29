"""
LLM client.
"""

from __future__ import annotations

from athena.ai.llm.models import (
    LLMRequest,
    LLMResponse,
)
from athena.ai.llm.provider import LLMProvider
from athena.ai.llm.provider_registry import ProviderRegistry


class LLMClient:
    """High-level interface for Athena AI generation."""

    def __init__(
        self,
        provider: LLMProvider | None = None,
        registry: ProviderRegistry | None = None,
    ) -> None:
        """Initialize client."""

        if registry is not None:
            self._registry = registry

        elif provider is not None:
            self._registry = ProviderRegistry()
            self._registry.register(provider)

        else:
            raise ValueError(
                "Either provider or registry must be supplied."
            )

    @property
    def registry(self) -> ProviderRegistry:
        """Return provider registry."""

        return self._registry

    @property
    def provider(self) -> LLMProvider:
        """Return active provider."""

        return self._registry.default()

    def analyze(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """
        Generate text using configured provider.
        """

        return self.provider.analyze(
            request,
        )
