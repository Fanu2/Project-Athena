"""
LLM runtime bootstrap.
"""

from __future__ import annotations

from athena.ai.llm.model_manager import (
    ModelManager,
)
from athena.ai.llm.provider_registry import (
    ProviderRegistry,
)
from athena.ai.llm.providers import (
    LMStudioProvider,
    OllamaProvider,
    OpenAIProvider,
)


class LLMRuntimeBootstrap:
    """Initialize LLM runtime dependencies."""

    def __init__(self) -> None:
        """Initialize runtime."""

        self._providers = ProviderRegistry()

        self._models = ModelManager(
            provider_registry=self._providers
        )

    def initialize(
        self,
    ) -> ModelManager:
        """Register providers and discover models."""

        self._providers.register(
            OllamaProvider()
        )

        self._providers.register(
            LMStudioProvider()
        )

        self._providers.register(
            OpenAIProvider()
        )

        self._discover_models_safely()

        return self._models

    def _discover_models_safely(
        self,
    ) -> None:
        """Discover available models without failing."""

        for provider_name in self._providers.names():
            try:
                self._models.discover_provider_models(
                    provider_name
                )

            except Exception:
                continue

    @property
    def providers(
        self,
    ) -> ProviderRegistry:
        """Return provider registry."""

        return self._providers

