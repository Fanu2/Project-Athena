"""
Runtime metrics storage for Athena LLM execution.
"""

from __future__ import annotations

from athena.ai.llm.runtime_metrics import RuntimeMetric


class RuntimeMetricsStore:
    """In-memory runtime metrics store."""

    def __init__(self) -> None:
        """Initialize store."""

        self._metrics: list[RuntimeMetric] = []

    def record(
        self,
        metric: RuntimeMetric,
    ) -> None:
        """Store runtime metric."""

        self._metrics.append(
            metric,
        )

    def metrics(
        self,
    ) -> list[RuntimeMetric]:
        """Return all metrics."""

        return list(
            self._metrics,
        )

    def for_model(
        self,
        model: str,
    ) -> list[RuntimeMetric]:
        """Return metrics for a model."""

        return [
            metric
            for metric in self._metrics
            if metric.model == model
        ]

    def average_latency(
        self,
        model: str,
    ) -> float | None:
        """Return average latency for model."""

        values = [
            metric.latency_ms
            for metric in self.for_model(
                model,
            )
        ]

        if not values:
            return None

        return sum(values) / len(values)

    def success_rate(
        self,
        model: str,
    ) -> float | None:
        """Return model success rate."""

        metrics = self.for_model(
            model,
        )

        if not metrics:
            return None

        successes = sum(
            1
            for metric in metrics
            if metric.success
        )

        return successes / len(metrics)