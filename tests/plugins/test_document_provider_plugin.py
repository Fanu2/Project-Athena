"""
Document provider plugin tests.
"""

from athena.plugins.examples.demo_document_provider_plugin import (
    DemoDocumentProviderPlugin,
)


def test_document_provider_plugin():

    plugin = DemoDocumentProviderPlugin()

    assert plugin.info.name == (
        "Demo Document Provider"
    )

    assert "document_provider" in (
        plugin.info.capabilities
    )

    provider = (
        plugin.create_provider()
    )

    assert provider.name == (
        "demo-document-provider"
    )

    assert "demo_parser" in (
        provider.capabilities
    )
