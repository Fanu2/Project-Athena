"""
Tests for evaluation gate facade.
"""

from athena.evaluation.benchmark_decision import (
    BenchmarkDecision,
    BenchmarkDecisionStatus,
)
from athena.evaluation.evaluation_gate import (
    EvaluationGate,
)
from athena.evaluation.quality_gate import (
    QualityGateStatus,
)


def test_evaluation_gate_pass() -> None:
    """PASS decision should produce PASS quality gate."""

    gate = EvaluationGate()

    decision = BenchmarkDecision(
        status=BenchmarkDecisionStatus.PASS,
        reasons=[],
    )

    result = gate.evaluate(
        decision,
    )

    assert result.status == (
        QualityGateStatus.PASS
    )

    assert result.can_release is True


def test_evaluation_gate_warning() -> None:
    """WARNING decision should produce WARNING gate."""

    gate = EvaluationGate()

    decision = BenchmarkDecision(
        status=BenchmarkDecisionStatus.WARNING,
        reasons=[
            "Latency increased significantly.",
        ],
    )

    result = gate.evaluate(
        decision,
    )

    assert result.status == (
        QualityGateStatus.WARNING
    )

    assert result.can_release is True

    assert (
        "Latency increased significantly."
        in result.checks
    )


def test_evaluation_gate_block() -> None:
    """BLOCK decision should prevent release."""

    gate = EvaluationGate()

    decision = BenchmarkDecision(
        status=BenchmarkDecisionStatus.BLOCK,
        reasons=[
            "Top-5 accuracy degraded.",
        ],
    )

    result = gate.evaluate(
        decision,
    )

    assert result.status == (
        QualityGateStatus.BLOCK
    )

    assert result.can_release is False

    assert (
        "Top-5 accuracy degraded."
        in result.checks
    )

