"""
Demo AI provider plugin.

Reference implementation for AI provider plugins.

This plugin demonstrates the contract only.
It is not a runtime provider.
Real runtime providers should implement
create_provider() and expose:

    "ai_provider"

capability.
"""

from __future__ import annotations

from athena.ai.llm.provider import (
    LLMProvider,
)

from athena.plugins.ai_provider_plugin import (
    AIProviderPlugin,
)

from athena.plugins.models import (
    PluginInfo,
)


class DemoAIProviderPlugin(
    AIProviderPlugin,
):
    """
    Example AI provider plugin.

    Demonstrates the plugin interface
    without registering a runtime provider.
    """


    @property
    def info(
        self,
    ) -> PluginInfo:
        """
        Return plugin metadata.
        """

        return PluginInfo(
            name="Demo AI Provider",
            version="1.0",
            description=(
                "Example AI provider plugin"
            ),
            capabilities=(
                "example_ai_provider",
            ),
        )


    def create_provider(
        self,
    ) -> LLMProvider:
        """
        Create provider instance.

        Demo only.

        Real plugins should return
        concrete providers such as:

            OllamaProvider()
            LMStudioProvider()
            CustomProvider()
        """

        raise NotImplementedError(
            "Demo provider has no runtime implementation"
        )
