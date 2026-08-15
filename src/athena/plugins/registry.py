"""
Plugin registry.

Stores and manages Athena plugins.
"""

from __future__ import annotations

from athena.plugins.base import AthenaPlugin


class PluginRegistry:
    """
    Maintains registered Athena plugins.
    """

    def __init__(
        self,
    ) -> None:

        self._plugins: list[AthenaPlugin] = []

    def register(
        self,
        plugin: AthenaPlugin,
    ) -> None:
        """
        Register a plugin.
        """

        self._plugins.append(
            plugin,
        )

    def plugins(
        self,
    ) -> list[AthenaPlugin]:
        """
        Return registered plugins.
        """

        return list(
            self._plugins,
        )

    def capabilities(
        self,
    ) -> tuple[str, ...]:
        """
        Return all plugin capabilities.
        """

        capabilities: list[str] = []

        for plugin in self._plugins:
            capabilities.extend(
                plugin.info.capabilities,
            )

        return tuple(
            capabilities,
        )

    def initialize_all(
        self,
        context,
    ) -> None:
        """
        Initialize all registered plugins.
        """

        for plugin in self._plugins:
            plugin.initialize(
                context,
            )

    def shutdown_all(
        self,
    ) -> None:
        """
        Shutdown all registered plugins.
        """

        for plugin in self._plugins:
            plugin.shutdown()
