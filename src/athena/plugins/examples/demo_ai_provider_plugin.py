"""
Demo AI provider plugin.

Reference implementation for AI provider plugins.
"""

from __future__ import annotations

from athena.ai.llm.provider import LLMProvider

from athena.plugins.ai_provider_plugin import (
    AIProviderPlugin,
)

from athena.plugins.models import (
    PluginInfo,
)


class DemoAIProviderPlugin(AIProviderPlugin):
    """
    Example AI provider plugin.
    """

    @property
    def info(
        self,
    ) -> PluginInfo:
        return PluginInfo(
            name="Demo AI Provider",
            version="1.0",
            description="Example AI provider plugin",
            capabilities=(
                "ai_provider",
            ),
        )

    def create_provider(
        self,
    ) -> LLMProvider:
        """
        Create provider instance.

        Demo only. Real plugins will
        return OllamaProvider, etc.
        """

        raise NotImplementedError(
            "Demo provider has no runtime implementation"
        )
