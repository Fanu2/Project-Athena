from athena.plugins.examples.demo_plugin import DemoPlugin


def test_demo_plugin_lifecycle():

    plugin = DemoPlugin()

    plugin.initialize(None)

    assert plugin.initialized is True

    plugin.shutdown()

    assert plugin.closed is True
