"""
Tests for benchmark quality gate model.
"""

from athena.evaluation.quality_gate import (
    QualityGateResult,
    QualityGateStatus,
)


def test_quality_gate_pass_allows_release() -> None:
    """PASS status should allow release."""

    result = QualityGateResult(
        status=QualityGateStatus.PASS,
        message="Benchmark quality maintained.",
        checks=[
            "Retrieval quality maintained.",
        ],
    )

    assert result.status == QualityGateStatus.PASS
    assert result.can_release is True


def test_quality_gate_warning_allows_release() -> None:
    """WARNING status should allow release with review."""

    result = QualityGateResult(
        status=QualityGateStatus.WARNING,
        message="Review benchmark warnings.",
        checks=[
            "Latency increased.",
        ],
    )

    assert result.status == QualityGateStatus.WARNING
    assert result.can_release is True


def test_quality_gate_block_prevents_release() -> None:
    """BLOCK status should prevent release."""

    result = QualityGateResult(
        status=QualityGateStatus.BLOCK,
        message="Benchmark regression detected.",
        checks=[
            "Top-5 accuracy degraded.",
            "MRR degraded.",
        ],
    )

    assert result.status == QualityGateStatus.BLOCK
    assert result.can_release is False

