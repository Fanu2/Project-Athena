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
from athena.ai.providers.provider_registry import (
    ProviderRegistry,
)


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
        """
        Infer model capabilities.

        Fallback only.
        Provider metadata has priority.
        """

        name = model_name.lower()

        return ModelCapabilities(
            chat=True,
            embeddings=(
                "embed" in name
            ),
            vision=(
                "llava" in name
                or "vision" in name
            ),
            local=True,
        )

    def _provider_model_capabilities(
        self,
        provider,
        model_name: str,
    ) -> ModelCapabilities:
        """
        Resolve model capabilities.

        Priority:
        1. Provider model mapping
        2. Provider defaults
        3. Name inference fallback
        """

        if hasattr(
            provider,
            "capabilities_for_model",
        ):
            capabilities = (
                provider.capabilities_for_model(
                    model_name,
                )
            )

            if capabilities:
                return ModelCapabilities(
                    chat="chat" in capabilities,
                    streaming=(
                        "streaming" in capabilities
                    ),
                    tools=(
                        "tools" in capabilities
                    ),
                    vision=(
                        "vision" in capabilities
                    ),
                    embeddings=(
                        "embedding" in capabilities
                    ),
                    reasoning=(
                        "reasoning" in capabilities
                    ),
                    reranking=(
                        "reranking" in capabilities
                    ),
                    local=True,
                )

        return self._infer_capabilities(
            model_name,
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

        if provider is None:
            return []

        try:
            provider_models = provider.list_models()

        except Exception:
            return []

        models: list[ModelInfo] = []

        for name in provider_models:

            model = ModelInfo(
                name=name,
                provider=provider_name,
                capabilities=(
                    self._provider_model_capabilities(
                        provider,
                        name,
                    )
                ),
            )

            models.append(
                model,
            )

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
