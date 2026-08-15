"""
AI provider plugin runtime bridge tests.
"""

from athena.ai.llm.runtime_bootstrap import (
    LLMRuntimeBootstrap,
)

from athena.ai.llm.provider import (
    LLMProvider,
)

from athena.plugins.ai_provider_plugin import (
    AIProviderPlugin,
)

from athena.plugins.models import (
    PluginInfo,
)

from athena.plugins.registry import (
    PluginRegistry,
)


class FakeLLMProvider(LLMProvider):
    """
    Fake provider for testing.
    """

    @property
    def provider_name(self):
        return "fake"

    @property
    def metadata(self):
        class Meta:
            display_name = "Fake Provider"

        return Meta()

    def capabilities(self):
        return {}

    def health(self):
        return True

    def list_models(self):
        return ["fake-model"]

    def analyze(
        self,
        *args,
        **kwargs,
    ):
        """
        Fake analysis implementation.
        """

        return None


class FakeAIProviderPlugin(AIProviderPlugin):
    """
    Fake AI provider plugin.
    """

    @property
    def info(self):
        return PluginInfo(
            name="Fake AI Provider",
            version="1.0",
            capabilities=(
                "ai_provider",
            ),
        )

    def create_provider(self):
        return FakeLLMProvider()


def test_plugin_provider_bridge():

    registry = PluginRegistry()

    registry.register(
        FakeAIProviderPlugin(),
    )

    runtime = LLMRuntimeBootstrap(
        plugin_registry=registry,
    )

    runtime.initialize()

    providers = [
        provider.provider_id
        for provider in runtime.runtime_providers.providers()
    ]

    assert "fake" in providers
