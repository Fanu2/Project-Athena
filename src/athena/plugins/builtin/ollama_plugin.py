"""
Built-in Ollama AI provider plugin.
"""

from __future__ import annotations

from athena.ai.llm.providers.ollama import (
    OllamaProvider,
)

from athena.plugins.ai_provider_plugin import (
    AIProviderPlugin,
)

from athena.plugins.models import (
    PluginInfo,
)


class OllamaAIProviderPlugin(AIProviderPlugin):
    """
    Provides the built-in Ollama LLM provider
    through the plugin system.
    """

    @property
    def info(
        self,
    ) -> PluginInfo:
        return PluginInfo(
            name="Ollama AI Provider",
            version="1.0",
            description=(
                "Ollama local LLM provider plugin"
            ),
            capabilities=(
                "ai_provider",
            ),
        )

    def create_provider(
        self,
    ) -> OllamaProvider:
        """
        Create Ollama runtime provider.
        """

        return OllamaProvider()

    def initialize(
        self,
        context,
    ) -> None:
        pass

    def shutdown(
        self,
    ) -> None:
        pass
