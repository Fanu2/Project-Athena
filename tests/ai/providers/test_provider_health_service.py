from athena.ai.providers.health_status import HealthStatus
from athena.ai.providers.provider_health_service import (
    ProviderHealthService,
)


def test_provider_health_service_reports_online():
    service = ProviderHealthService()

    result = service.check_provider(
        provider_id="ollama",
        model="qwen3",
        capabilities=(
            "chat",
            "embedding",
        ),
    )

    assert result.provider_id == "ollama"
    assert result.status == HealthStatus.ONLINE
    assert result.active_model == "qwen3"
    assert "chat" in result.capabilities