"""
Built-in Athena plugins.
"""

from __future__ import annotations

from athena.plugins.examples.demo_plugin import (
    DemoPlugin,
)

from athena.plugins.examples.demo_ai_provider_plugin import (
    DemoAIProviderPlugin,
)

from athena.plugins.examples.demo_document_provider_plugin import (
    DemoDocumentProviderPlugin,
)

from athena.plugins.builtin.ollama_plugin import (
    OllamaAIProviderPlugin,
)

from athena.plugins.registry import (
    PluginRegistry,
)


def register_builtin_plugins(
    registry: PluginRegistry,
) -> None:
    """
    Register Athena built-in plugins.
    """

    registry.register(
        DemoPlugin(),
    )

    registry.register(
        DemoAIProviderPlugin(),
    )

    registry.register(
        DemoDocumentProviderPlugin(),
    )

    registry.register(
        OllamaAIProviderPlugin(),
    )
