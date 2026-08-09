"""
Routing score model for Athena LLM selection.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RoutingScore:
    """Score breakdown for model routing."""

    model: str

    capability_score: float = 0.0

    quality_score: float = 0.0

    local_score: float = 0.0

    context_score: float = 0.0

    health_score: float = 0.0

    policy_score: float = 0.0

    @property
    def total(self) -> float:
        """Return combined routing score."""

        return (
            self.capability_score
            + self.quality_score
            + self.local_score
            + self.context_score
            + self.health_score
            + self.policy_score
        )