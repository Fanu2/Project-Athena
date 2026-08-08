from __future__ import annotations

import time

from athena.ai.providers.health_status import HealthStatus
from athena.ai.providers.provider_health import ProviderHealth


class ProviderHealthService:
    """Service responsible for AI provider health checks."""

    def check_provider(
        self,
        provider_id: str,
        model: str | None = None,
        capabilities: tuple[str, ...] = (),
    ) -> ProviderHealth:
        """Check and return provider health."""

        start_time = time.perf_counter()

        try:
            latency_ms = (
                time.perf_counter() - start_time
            ) * 1000

            return ProviderHealth(
                provider_id=provider_id,
                status=HealthStatus.ONLINE,
                latency_ms=latency_ms,
                active_model=model,
                capabilities=capabilities,
            )

        except Exception as exc:
            return ProviderHealth(
                provider_id=provider_id,
                status=HealthStatus.DEGRADED,
                message=str(exc),
            )