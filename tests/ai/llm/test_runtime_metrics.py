"""
Tests for runtime metrics.
"""

from __future__ import annotations

from athena.ai.llm.runtime_metrics import RuntimeMetric
from athena.ai.llm.runtime_metrics_store import (
    RuntimeMetricsStore,
)


def test_record_runtime_metric() -> None:
    store = RuntimeMetricsStore()

    store.record(
        RuntimeMetric(
            model="qwen3:4b",
            provider="ollama",
            latency_ms=120.0,
        )
    )

    assert len(
        store.metrics()
    ) == 1


def test_average_latency() -> None:
    store = RuntimeMetricsStore()

    store.record(
        RuntimeMetric(
            model="qwen3:4b",
            provider="ollama",
            latency_ms=100.0,
        )
    )

    store.record(
        RuntimeMetric(
            model="qwen3:4b",
            provider="ollama",
            latency_ms=200.0,
        )
    )

    assert (
        store.average_latency(
            "qwen3:4b"
        )
        == 150.0
    )


def test_success_rate() -> None:
    store = RuntimeMetricsStore()

    store.record(
        RuntimeMetric(
            model="qwen3:4b",
            provider="ollama",
            latency_ms=100.0,
            success=True,
        )
    )

    store.record(
        RuntimeMetric(
            model="qwen3:4b",
            provider="ollama",
            latency_ms=100.0,
            success=False,
        )
    )

    assert (
        store.success_rate(
            "qwen3:4b"
        )
        == 0.5
    )