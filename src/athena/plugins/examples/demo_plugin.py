"""
Demo Athena plugin.

Reference implementation for plugin framework.
"""

from __future__ import annotations

from athena.plugins.base import AthenaPlugin
from athena.plugins.models import PluginInfo


class DemoPlugin(AthenaPlugin):
    """
    Example plugin implementation.
    """

    def __init__(self) -> None:
        self.initialized = False
        self.closed = False

    @property
    def info(self) -> PluginInfo:
        return PluginInfo(
            name="Demo Plugin",
            version="1.0",
            description="Reference Athena plugin",
            capabilities=(
                "example",
            ),
        )

    def initialize(
        self,
        context,
    ) -> None:
        self.initialized = True

    def shutdown(
        self,
    ) -> None:
        self.closed = True
