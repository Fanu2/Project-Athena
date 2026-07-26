"""
Benchmark decision engine.
"""

from __future__ import annotations

from athena.evaluation.benchmark_comparator import (
    BenchmarkComparison,
)
from athena.evaluation.benchmark_decision import (
    BenchmarkDecision,
    BenchmarkDecisionStatus,
)


class BenchmarkDecisionEngine:
    """Convert benchmark comparison into a decision."""

    def decide(
        self,
        comparison: BenchmarkComparison,
    ) -> BenchmarkDecision:
        """Create a release decision."""

        if not comparison.degraded:
            return BenchmarkDecision(
                status=BenchmarkDecisionStatus.PASS,
                reasons=[],
            )

        reasons = comparison.warnings

        if len(reasons) >= 2:
            return BenchmarkDecision(
                status=BenchmarkDecisionStatus.BLOCK,
                reasons=reasons,
            )

        return BenchmarkDecision(
            status=BenchmarkDecisionStatus.WARNING,
            reasons=reasons,
        )
