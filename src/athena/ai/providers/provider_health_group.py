"""
Provider health aggregation model.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from athena.ai.providers.provider_health import ProviderHealth


@dataclass
class ProviderHealthGroup:
    """Aggregated health information for a provider."""

    provider_id: str

    status: str

    models: list[str] = field(
        default_factory=list,
    )

    capabilities: set[str] = field(
        default_factory=set,
    )

    latency_ms: float | None = None

    @classmethod
    def from_health(
        cls,
        health: list[ProviderHealth],
    ) -> list["ProviderHealthGroup"]:
        """Aggregate model health by provider."""

        groups: dict[str, ProviderHealthGroup] = {}

        for item in health:

            if item.provider_id not in groups:
                groups[item.provider_id] = cls(
                    provider_id=item.provider_id,
                    status=item.status.value,
                    latency_ms=item.latency_ms,
                )

            group = groups[item.provider_id]

            if item.active_model:
                group.models.append(
                    item.active_model,
                )

            group.capabilities.update(
                item.capabilities,
            )

        return list(groups.values())