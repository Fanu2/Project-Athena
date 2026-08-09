"""
Model manager service.
"""

from __future__ import annotations

from athena.ai.llm.capabilities import ModelCapabilities
from athena.ai.llm.metadata import ProviderMetadata
from athena.ai.llm.model_info import ModelInfo
from athena.ai.llm.model_profiles import DEFAULT_MODEL_PROFILES
from athena.ai.llm.model_profile import ModelProfile
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

    def _infer_capabilities(
        self,
        model_name: str,
    ) -> ModelCapabilities:
        """Infer model capabilities."""

        name = model_name.lower()

        return ModelCapabilities(
            chat=True,
            vision=(
                "llava" in name
                or "vision" in name
            ),
            embeddings=(
                "embed" in name
            ),
            local=True,
        )

    def register_model(
        self,
        model: ModelInfo,
    ) -> None:
        """Register a model."""

        self._models.register(
            model,
        )

    def models(
        self,
    ) -> list[ModelInfo]:
        """Return available models."""

        return self._models.models()

    def models_by_capability(
        self,
        capability: str,
    ) -> list[ModelInfo]:
        """Return models supporting capability."""

        return self._models.by_capability(
            capability,
        )

    def get_model(
        self,
        name: str,
    ) -> ModelInfo:
        """Return model."""

        return self._models.get(
            name,
        )

    def set_active_model(
        self,
        name: str,
    ) -> None:
        """Set active model."""

        self._models.set_active(
            name,
        )

    def active_model(
        self,
    ) -> ModelInfo:
        """Return active model."""

        return self._models.active()

    def get_profile(
        self,
        capability: str,
    ) -> ModelProfile:
        """Return default profile for capability."""

        for profile in DEFAULT_MODEL_PROFILES:
            if profile.capability == capability:
                return profile

        raise ValueError(
            f"No model profile for capability: {capability}"
        )

    def discover_provider_models(
        self,
        provider_name: str,
    ) -> list[ModelInfo]:
        """Discover models from provider."""

        provider = self._providers.get(
            provider_name,
        )

        try:
            provider_models = provider.list_models()

        except Exception:
            return []

        models = [
            ModelInfo(
                name=name,
                provider=provider_name,
                capabilities=(
                    self._infer_capabilities(name)
                ),
            )
            for name in provider_models
        ]

        for model in models:
            if not self._models.exists(
                model.name,
            ):
                self._models.register(
                    model,
                )

        return models

    def discover_all_models(
        self,
    ) -> list[ModelInfo]:
        """Discover models from all providers."""

        discovered: list[ModelInfo] = []

        for provider_name in self._providers.names():
            discovered.extend(
                self.discover_provider_models(
                    provider_name,
                )
            )

        self._models.select_best_model()

        return discovered

    def has_model(
        self,
        name: str,
    ) -> bool:
        """Return whether model exists."""

        return self._models.exists(
            name,
        )

    def provider_metadata(
        self,
        model: ModelInfo,
    ) -> ProviderMetadata:
        """Return metadata for model provider."""

        provider = self._providers.get(
            model.provider,
        )

        return provider.metadata