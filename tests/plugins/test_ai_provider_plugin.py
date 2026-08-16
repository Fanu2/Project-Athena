"""
AI provider plugin contract tests.
"""

from athena.plugins.examples.demo_ai_provider_plugin import (
    DemoAIProviderPlugin,
)


def test_ai_provider_plugin_metadata():

    plugin = DemoAIProviderPlugin()

    assert plugin.info.name == (
        "Demo AI Provider"
    )

    assert "example_ai_provider" in (
        plugin.info.capabilities
    )
