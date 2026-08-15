"""
Document provider runtime bridge tests.
"""

from athena.knowledge.acquisition.services.provider_manager import (
    ProviderManager,
)

from athena.plugins.registry import (
    PluginRegistry,
)

from athena.plugins.examples.demo_document_provider_plugin import (
    DemoDocumentProviderPlugin,
)


def test_document_provider_plugin_bridge():

    registry = PluginRegistry()

    registry.register(
        DemoDocumentProviderPlugin(),
    )

    manager = ProviderManager(
        plugin_registry=registry,
    )

    manager.register_plugin_providers()

    result = manager.execute(
        "demo_parser",
        "sample.txt",
    )

    assert result["capability"] == (
        "demo_parser"
    )

    assert result["input"] == (
        "sample.txt"
    )
