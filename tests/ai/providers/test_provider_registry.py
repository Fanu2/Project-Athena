from athena.ai.providers.provider import Provider
from athena.ai.providers.provider_registry import (
    ProviderRegistry,
)


def test_provider_registry_registers_provider():
    registry = ProviderRegistry()

    provider = Provider(
        provider_id="ollama",
        name="Ollama",
        endpoint="http://localhost:11434",
        models=[
            "qwen3:4b",
            "llama:latest",
        ],
        capabilities={
            "chat",
            "embedding",
        },
    )

    registry.register(provider)

    result = registry.get("ollama")

    assert result is not None
    assert result.name == "Ollama"
    assert result.endpoint == "http://localhost:11434"
    assert "qwen3:4b" in result.models


def test_provider_registry_lists_enabled_providers():
    registry = ProviderRegistry()

    registry.register(
        Provider(
            provider_id="ollama",
            name="Ollama",
        )
    )

    registry.register(
        Provider(
            provider_id="disabled",
            name="Disabled Provider",
            enabled=False,
        )
    )

    providers = registry.enabled_providers()

    assert len(providers) == 1
    assert providers[0].provider_id == "ollama"