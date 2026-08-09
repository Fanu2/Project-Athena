"""
Model scoring service for Athena runtime routing.
"""

from __future__ import annotations

from athena.ai.llm.model_info import ModelInfo
from athena.ai.llm.routing_score import RoutingScore
from athena.ai.llm.runtime_metrics_store import (
    RuntimeMetricsStore,
)


class ModelScoringService:
    """Score models for runtime selection."""

    def __init__(
        self,
        metrics_store: RuntimeMetricsStore | None = None,
    ) -> None:
        """Initialize scorer."""

        self._metrics = (
            metrics_store
            if metrics_store is not None
            else RuntimeMetricsStore()
        )

    def score(
        self,
        model: ModelInfo,
    ) -> RoutingScore:
        """Calculate routing score."""

        return RoutingScore(
            model=model.name,
            capability_score=(
                50.0
                if model.capabilities.chat
                else 0.0
            ),
            quality_score=(
                10.0
                if model.capabilities.reasoning
                else 0.0
            ),
            local_score=(
                5.0
                if model.capabilities.local
                else 0.0
            ),
            context_score=self._context_score(
                model,
            ),
            health_score=self._runtime_score(
                model,
            ),
        )

    def rank(
        self,
        models: list[ModelInfo],
    ) -> list[ModelInfo]:
        """Rank models by routing score."""

        return sorted(
            models,
            key=lambda model: self.score(model).total,
            reverse=True,
        )

    def best(
        self,
        models: list[ModelInfo],
    ) -> ModelInfo:
        """Return highest scoring model."""

        if not models:
            raise ValueError(
                "No models available."
            )

        return self.rank(models)[0]

    def _runtime_score(
        self,
        model: ModelInfo,
    ) -> float:
        """Score runtime performance."""

        score = 0.0

        success_rate = (
            self._metrics.success_rate(
                model.name,
            )
        )

        if success_rate is not None:
            score += success_rate * 10.0

        latency = (
            self._metrics.average_latency(
                model.name,
            )
        )

        if latency is not None:
            if latency < 200:
                score += 5.0
            elif latency < 500:
                score += 3.0
            else:
                score += 1.0

        return score

    def _context_score(
        self,
        model: ModelInfo,
    ) -> float:
        """Score context window."""

        if model.context_window >= 32768:
            return 5.0

        if model.context_window >= 8192:
            return 3.0

        if model.context_window > 0:
            return 1.0

        return 0.0