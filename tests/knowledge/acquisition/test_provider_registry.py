from athena.knowledge.acquisition.registry.provider_registry import (
    ProviderRegistry,
)

from athena.knowledge.acquisition.contracts.provider import (
    Provider,
)


class TestProvider(Provider):

    @property
    def name(self):
        return "test"

    @property
    def capabilities(self):
        return [
            "pdf_parser",
        ]

    def execute(
        self,
        capability,
        input_data,
    ):
        return input_data


def test_register_provider():

    registry = ProviderRegistry()

    provider = TestProvider()

    registry.register(provider)

    assert (
        registry.get_provider("pdf_parser")
        == provider
    )


def test_capabilities():

    registry = ProviderRegistry()

    registry.register(TestProvider())

    assert "pdf_parser" in registry.capabilities()