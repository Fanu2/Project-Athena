"""
Model manager service.
"""

from __future__ import annotations

from athena.ai.llm.metadata import ProviderMetadata
from athena.ai.llm.model_info import ModelInfo
from athena.ai.llm.model_registry import ModelRegistry
from athena.ai.llm.provider_registry import ProviderRegistry


class ModelManager:
    """Manage available LLM models."""

    def __init__(
        self,
        model_registry: ModelRegistry | None = None,
        provider_registry: ProviderRegistry | None = None,
    ) -> None:
        """Initialize model manager."""

        self._models = (
            model_registry
            if model_registry is not None
            else ModelRegistry()
        )

        self._providers = (
            provider_registry
            if provider_registry is not None
            else ProviderRegistry()
        )

    def register_model(
        self,
        model: ModelInfo,
    ) -> None:
        """Register a model."""

        self._models.register(model)

    def models(self) -> list[ModelInfo]:
        """Return available models."""

        return self._models.models()

    def get_model(
        self,
        name: str,
    ) -> ModelInfo:
        """Return model."""

        return self._models.get(name)

    def set_active_model(
        self,
        name: str,
    ) -> None:
        """Set active model."""

        self._models.set_active(name)

    def active_model(self) -> ModelInfo:
        """Return active model."""

        return self._models.active()

    def discover_provider_models(
        self,
        provider_name: str,
    ) -> list[ModelInfo]:
        """Discover models from provider."""

        provider = self._providers.get(provider_name)

        models = [
            ModelInfo(
                name=name,
                provider=provider_name,
            )
            for name in provider.list_models()
        ]

        for model in models:
            if not self._models.exists(model.name):
                self._models.register(model)

        return models

    def discover_all_models(self) -> list[ModelInfo]:
        """Discover models from all providers."""

        discovered: list[ModelInfo] = []

        for provider_name in self._providers.names():
            discovered.extend(
                self.discover_provider_models(
                    provider_name
                )
            )

        return discovered

    def has_model(
        self,
        name: str,
    ) -> bool:
        """Return whether model exists."""

        return self._models.exists(name)

    def provider_metadata(
        self,
        model: ModelInfo,
    ) -> ProviderMetadata:
        """Return metadata for model provider."""

        provider = self._providers.get(
            model.provider
        )

        return provider.metadata

