"""
Demo document provider plugin.

Reference implementation for document provider plugins.
"""

from __future__ import annotations

from typing import Any

from athena.knowledge.acquisition.contracts.provider import (
    Provider,
)

from athena.plugins.document_provider_plugin import (
    DocumentProviderPlugin,
)

from athena.plugins.models import (
    PluginInfo,
)


class DemoDocumentProvider(
    Provider,
):
    """
    Fake knowledge acquisition provider.
    """

    @property
    def name(
        self,
    ) -> str:
        return "demo-document-provider"

    @property
    def capabilities(
        self,
    ) -> list[str]:
        return [
            "demo_parser",
        ]

    def execute(
        self,
        capability: str,
        input_data: Any,
    ) -> Any:
        return {
            "capability": capability,
            "input": input_data,
        }


class DemoDocumentProviderPlugin(
    DocumentProviderPlugin,
):
    """
    Example document provider plugin.
    """

    @property
    def info(
        self,
    ) -> PluginInfo:

        return PluginInfo(
            name="Demo Document Provider",
            version="1.0",
            description="Example knowledge provider plugin",
            capabilities=(
                "document_provider",
            ),
        )

    def create_provider(
        self,
    ) -> Provider:

        return DemoDocumentProvider()
