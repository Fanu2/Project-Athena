"""
Built-in plugin registry tests.
"""

from athena.plugins.builtin.registry import (
    register_builtin_plugins,
)

from athena.plugins.registry import (
    PluginRegistry,
)


def test_builtin_registry_contains_ollama():

    registry = PluginRegistry()

    register_builtin_plugins(
        registry,
    )

    names = [
        plugin.info.name
        for plugin in registry.plugins()
    ]

    assert "Ollama AI Provider" in names
