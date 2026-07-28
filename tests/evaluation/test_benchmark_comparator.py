"""
Tests for benchmark comparator.
"""

from athena.evaluation.benchmark_comparator import (
    BenchmarkComparator,
)
from athena.evaluation.benchmark_models import (
    BenchmarkSummary,
)


def create_summary(
    *,
    top5_accuracy: float = 0.96,
    mean_reciprocal_rank: float = 0.73,
    average_latency_ms: float = 140.0,
) -> BenchmarkSummary:
    """Create benchmark summary fixture."""

    return BenchmarkSummary(
        total_questions=25,
        successful_retrievals=25,
        failed_retrievals=0,
        top1_accuracy=0.60,
        top3_accuracy=0.88,
        top5_accuracy=top5_accuracy,
        mean_reciprocal_rank=mean_reciprocal_rank,
        average_latency_ms=average_latency_ms,
    )


def test_comparator_detects_stable_result() -> None:
    """No warnings should be produced for stable results."""

    comparator = BenchmarkComparator()

    previous = create_summary()

    current = create_summary(
        top5_accuracy=0.97,
        mean_reciprocal_rank=0.74,
        average_latency_ms=145.0,
    )

    result = comparator.compare(
        previous,
        current,
    )

    assert result.degraded is False
    assert result.improved is True
    assert result.warnings == []


def test_comparator_detects_accuracy_regression() -> None:
    """Accuracy degradation should generate warning."""

    comparator = BenchmarkComparator()

    previous = create_summary(
        top5_accuracy=0.96,
    )

    current = create_summary(
        top5_accuracy=0.90,
    )

    result = comparator.compare(
        previous,
        current,
    )

    assert result.degraded is True
    assert result.improved is False
    assert "Top-5 accuracy degraded." in result.warnings


def test_comparator_detects_mrr_regression() -> None:
    """MRR degradation should generate warning."""

    comparator = BenchmarkComparator()

    previous = create_summary(
        mean_reciprocal_rank=0.75,
    )

    current = create_summary(
        mean_reciprocal_rank=0.69,
    )

    result = comparator.compare(
        previous,
        current,
    )

    assert result.degraded is True
    assert "MRR degraded." in result.warnings


def test_comparator_detects_latency_regression() -> None:
    """Large latency increase should generate warning."""

    comparator = BenchmarkComparator()

    previous = create_summary(
        average_latency_ms=100.0,
    )

    current = create_summary(
        average_latency_ms=130.0,
    )

    result = comparator.compare(
        previous,
        current,
    )

    assert result.degraded is True
    assert "Latency increased significantly." in result.warnings

