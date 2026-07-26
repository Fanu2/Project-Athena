"""
Tests for benchmark quality gate service.
"""

from athena.evaluation.benchmark_decision import (
    BenchmarkDecision,
    BenchmarkDecisionStatus,
)
from athena.evaluation.quality_gate import (
    QualityGateStatus,
)
from athena.evaluation.quality_gate_service import (
    QualityGateService,
)


def test_quality_gate_service_pass() -> None:
    """PASS decision should create PASS gate."""

    service = QualityGateService()

    decision = BenchmarkDecision(
        status=BenchmarkDecisionStatus.PASS,
        reasons=[],
    )

    result = service.evaluate(
        decision,
    )

    assert result.status == QualityGateStatus.PASS
    assert result.can_release is True
    assert result.checks == [
        "No regression detected.",
    ]


def test_quality_gate_service_warning() -> None:
    """WARNING decision should create WARNING gate."""

    service = QualityGateService()

    decision = BenchmarkDecision(
        status=BenchmarkDecisionStatus.WARNING,
        reasons=[
            "Latency increased significantly.",
        ],
    )

    result = service.evaluate(
        decision,
    )

    assert result.status == QualityGateStatus.WARNING
    assert result.can_release is True
    assert (
        "Latency increased significantly."
        in result.checks
    )


def test_quality_gate_service_block() -> None:
    """BLOCK decision should prevent release."""

    service = QualityGateService()

    decision = BenchmarkDecision(
        status=BenchmarkDecisionStatus.BLOCK,
        reasons=[
            "Top-5 accuracy degraded.",
            "MRR degraded.",
        ],
    )

    result = service.evaluate(
        decision,
    )

    assert result.status == QualityGateStatus.BLOCK
    assert result.can_release is False
    assert len(result.checks) == 2
