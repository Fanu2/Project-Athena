"""
Ollama AI provider plugin tests.
"""

from athena.plugins.builtin.ollama_plugin import (
    OllamaAIProviderPlugin,
)

from athena.ai.llm.providers.ollama import (
    OllamaProvider,
)


def test_ollama_plugin_metadata():

    plugin = OllamaAIProviderPlugin()

    assert plugin.info.name == (
        "Ollama AI Provider"
    )

    assert "ai_provider" in (
        plugin.info.capabilities
    )


def test_ollama_plugin_creates_provider():

    plugin = OllamaAIProviderPlugin()

    provider = (
        plugin.create_provider()
    )

    assert isinstance(
        provider,
        OllamaProvider,
    )
