"""
Athena Provider Manager

Controls provider discovery and execution.
"""

from typing import Any

from ..contracts.provider import Provider
from ..registry.provider_registry import ProviderRegistry

from athena.plugins.registry import PluginRegistry


class ProviderManager:
    """
    Manages Athena capability providers.
    """

    def __init__(
        self,
        registry: ProviderRegistry | None = None,
        plugin_registry: PluginRegistry | None = None,
    ) -> None:

        self.registry = (
            registry
            if registry is not None
            else ProviderRegistry()
        )

        self._plugin_registry = (
            plugin_registry
        )

    def register(
        self,
        provider: Provider,
    ) -> None:
        """
        Register provider.
        """

        self.registry.register(provider)

    def register_plugin_providers(
        self,
    ) -> None:
        """
        Register document providers supplied by plugins.
        """

        if self._plugin_registry is None:
            return

        for plugin in self._plugin_registry.plugins():

            if (
                "document_provider"
                not in plugin.info.capabilities
            ):
                continue

            provider = (
                plugin.create_provider()
            )

            self.register(
                provider,
            )

    def execute(
        self,
        capability: str,
        input_data: Any,
    ) -> Any:
        """
        Execute capability provider.
        """

        provider = self.registry.get_provider(
            capability
        )

        if provider is None:
            raise ValueError(
                f"No provider found for capability: {capability}"
            )

        return provider.execute(
            capability,
            input_data,
        )