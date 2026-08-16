"""
LLM runtime bootstrap.

Initializes:
- LLM execution providers
- Model manager
- Runtime provider registry
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
    OpenAICompatibleProvider,
    OpenAIProvider,
)

from athena.ai.providers.provider_adapter import (
    ProviderAdapter,
)

from athena.ai.providers.provider_registry import (
    ProviderRegistry as RuntimeProviderRegistry,
)

from athena.settings import (
    LLMSettings,
)

from athena.plugins.registry import (
    PluginRegistry,
)


class LLMRuntimeBootstrap:
    """Initialize LLM runtime dependencies."""

    def __init__(
        self,
        plugin_registry: PluginRegistry | None = None,
    ) -> None:
        """Initialize runtime."""

        #
        # LLM execution providers
        #

        self._providers = ProviderRegistry()

        #
        # Athena runtime provider platform
        #

        self._runtime_providers = (
            RuntimeProviderRegistry()
        )

        #
        # Model management
        #

        self._models = ModelManager(
            provider_registry=self._providers,
        )

        self._initialized = False

        #
        # Optional plugin registry
        #
        # Plugin providers will be connected later.
        #

        self._plugin_registry = (
            plugin_registry
        )

    def initialize(
        self,
    ) -> ModelManager:
        """
        Register providers and discover models.

        Initialization is idempotent.
        """

        if self._initialized:
            return self._models

        self._register_provider(
            OllamaProvider()
        )

        self._register_provider(
            LMStudioProvider()
        )

        self._register_provider(
            OpenAIProvider()
        )

        self._register_provider(
            OpenAICompatibleProvider(
                settings=LLMSettings(
                    provider="llama-cpp-local",
                    model="Qwen3.5-2B-Q4_K_M.gguf",
                    base_url=(
                        "http://localhost:11434"
                    ),
                )
            )
        )

        self._register_plugin_providers()

        self._discover_models_safely()

        self._initialized = True

        return self._models

    def _register_provider(
        self,
        provider,
    ) -> None:
        """
        Register execution provider
        and runtime provider metadata.
        """

        self._providers.register(
            provider,
        )

        self._runtime_providers.register(
            ProviderAdapter.from_llm_provider(
                provider,
            )
        )

    def _register_plugin_providers(
        self,
    ) -> None:
        """
        Register providers supplied by plugins.

        Uses the existing provider registration path.
        """

        if self._plugin_registry is None:
            return

        for plugin in self._plugin_registry.plugins():

            if (
                "ai_provider"
                not in plugin.info.capabilities
            ):
                continue

            provider = (
                plugin.create_provider()
            )

            if self._providers.exists(
                provider.provider_name,
            ):
                continue

            self._register_provider(
                provider,
            )

    def _discover_models_safely(
        self,
    ) -> None:
        """Discover models without failing."""

        for provider_name in (
            self._providers.names()
        ):
            try:
                self._models.discover_provider_models(
                    provider_name,
                )

            except Exception:
                continue

        self._models._models.select_best_model()

    @property
    def providers(
        self,
    ) -> ProviderRegistry:
        """Return LLM execution provider registry."""

        return self._providers

    @property
    def runtime_providers(
        self,
    ) -> RuntimeProviderRegistry:
        """Return Athena runtime provider registry."""

        return self._runtime_providers

    @property
    def models(
        self,
    ) -> ModelManager:
        """Return initialized model manager."""

        return self._models
