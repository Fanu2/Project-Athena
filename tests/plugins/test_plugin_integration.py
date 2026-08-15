"""
Plugin integration tests.
"""

from athena.core.application_context import (
    ApplicationContext,
)


def test_builtin_plugins_registered():
    """
    Built-in plugins should be registered
    in application context.
    """

    context = ApplicationContext()

    capabilities = (
        context.plugin_registry.capabilities()
    )

    assert "example" in capabilities
