from __future__ import annotations

from dataclasses import dataclass

from athena.ai.providers.health_status import HealthStatus


@dataclass(frozen=True)
class ProviderHealth:
    """Runtime health information for an AI provider."""

    provider_id: str

    status: HealthStatus

    latency_ms: float | None = None

    active_model: str | None = None

    capabilities: tuple[str, ...] = ()

    message: str | None = None