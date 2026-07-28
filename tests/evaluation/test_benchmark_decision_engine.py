"""
Tests for benchmark decision engine.
"""

from athena.evaluation.benchmark_comparator import (
    BenchmarkComparison,
)
from athena.evaluation.benchmark_decision import (
    BenchmarkDecisionStatus,
)
from athena.evaluation.benchmark_decision_engine import (
    BenchmarkDecisionEngine,
)


def test_decision_engine_returns_pass() -> None:
    """No degradation should pass."""

    engine = BenchmarkDecisionEngine()

    comparison = BenchmarkComparison(
        improved=True,
        degraded=False,
        warnings=[],
    )

    decision = engine.decide(
        comparison,
    )

    assert decision.status == (
        BenchmarkDecisionStatus.PASS
    )

    assert decision.allowed_to_freeze is True

    assert decision.reasons == []


def test_decision_engine_returns_warning() -> None:
    """Single regression should warn."""

    engine = BenchmarkDecisionEngine()

    comparison = BenchmarkComparison(
        improved=False,
        degraded=True,
        warnings=[
            "Top-5 accuracy degraded.",
        ],
    )

    decision = engine.decide(
        comparison,
    )

    assert decision.status == (
        BenchmarkDecisionStatus.WARNING
    )

    assert decision.allowed_to_freeze is True

    assert (
        "Top-5 accuracy degraded."
        in decision.reasons
    )


def test_decision_engine_returns_block() -> None:
    """Multiple regressions should block."""

    engine = BenchmarkDecisionEngine()

    comparison = BenchmarkComparison(
        improved=False,
        degraded=True,
        warnings=[
            "Top-5 accuracy degraded.",
            "Latency increased significantly.",
        ],
    )

    decision = engine.decide(
        comparison,
    )

    assert decision.status == (
        BenchmarkDecisionStatus.BLOCK
    )

    assert decision.allowed_to_freeze is False

    assert len(decision.reasons) == 2

