"""
Tests for Athena plugin foundation.
"""

from athena.plugins.base import AthenaPlugin
from athena.plugins.models import PluginInfo
from athena.plugins.registry import PluginRegistry


class DemoPlugin(AthenaPlugin):
    """Example plugin for testing."""

    @property
    def info(self) -> PluginInfo:
        return PluginInfo(
            name="Demo",
            version="1.0",
            description="Test plugin",
        )


def test_plugin_info():
    """
    Plugin metadata should be available.
    """

    info = PluginInfo(
        name="Test",
        version="1.0",
    )

    assert info.name == "Test"
    assert info.version == "1.0"


def test_plugin_registry():
    """
    Registry should store plugins.
    """

    registry = PluginRegistry()

    plugin = DemoPlugin()

    registry.register(
        plugin,
    )

    assert len(
        registry.plugins(),
    ) == 1

    assert registry.plugins()[0].info.name == "Demo"
