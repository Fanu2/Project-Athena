"""
Model scoring service for Athena runtime routing.
"""

from __future__ import annotations

from athena.ai.llm.model_info import ModelInfo
from athena.ai.llm.model_policy import ModelPolicy
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
        policy: ModelPolicy | None = None,
    ) -> RoutingScore:
        """Calculate routing score."""

        return RoutingScore(
            model=model.name,
            capability_score=self._capability_score(
                model,
            ),
            quality_score=self._quality_score(
                model,
            ),
            local_score=self._local_score(
                model,
            ),
            context_score=self._context_score(
                model,
            ),
            health_score=self._runtime_score(
                model,
            ),
            policy_score=self._policy_score(
                model,
                policy,
            ),
        )

    def rank(
        self,
        models: list[ModelInfo],
        policy: ModelPolicy | None = None,
    ) -> list[ModelInfo]:
        """Rank models by routing score."""

        return sorted(
            models,
            key=lambda model: self.score(
                model,
                policy,
            ).total,
            reverse=True,
        )

    def best(
        self,
        models: list[ModelInfo],
        policy: ModelPolicy | None = None,
    ) -> ModelInfo:
        """Return highest scoring model."""

        if not models:
            raise ValueError(
                "No models available."
            )

        return self.rank(
            models,
            policy,
        )[0]

    def _capability_score(
        self,
        model: ModelInfo,
    ) -> float:
        """Score basic capability support."""

        return (
            50.0
            if model.capabilities.chat
            else 0.0
        )

    def _quality_score(
        self,
        model: ModelInfo,
    ) -> float:
        """Score model quality."""

        score = 0.0

        if model.capabilities.reasoning:
            score += 10.0

        return score

    def _local_score(
        self,
        model: ModelInfo,
    ) -> float:
        """Score local execution preference."""

        return (
            5.0
            if model.capabilities.local
            else 0.0
        )

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

    def _policy_score(
        self,
        model: ModelInfo,
        policy: ModelPolicy | None,
    ) -> float:
        """Score model according to policy."""

        if policy is None:
            return 0.0

        score = 0.0

        if (
            policy.prefer_local
            and model.capabilities.local
        ):
            score += 10.0

        if (
            policy.require_reasoning
            and model.capabilities.reasoning
        ):
            score += 20.0

        if (
            policy.require_vision
            and model.capabilities.vision
        ):
            score += 20.0

        if (
            policy.require_embeddings
            and model.capabilities.embeddings
        ):
            score += 20.0

        if (
            policy.latency_priority
            and model.capabilities.local
        ):
            score += 5.0

        if (
            policy.quality_priority
            and model.capabilities.reasoning
        ):
            score += 5.0

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