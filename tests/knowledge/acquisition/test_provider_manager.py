from athena.knowledge.acquisition.services.provider_manager import (
    ProviderManager,
)

from athena.knowledge.acquisition.contracts.provider import (
    Provider,
)


class EchoProvider(Provider):

    @property
    def name(self):
        return "echo"

    @property
    def capabilities(self):
        return [
            "echo"
        ]

    def execute(
        self,
        capability,
        input_data,
    ):
        return input_data


def test_provider_execution():

    manager = ProviderManager()

    manager.register(
        EchoProvider()
    )

    result = manager.execute(
        "echo",
        "athena",
    )

    assert result == "athena"