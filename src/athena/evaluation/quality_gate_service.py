"""
Benchmark quality gate service.
"""

from __future__ import annotations

from athena.evaluation.benchmark_decision import (
    BenchmarkDecisionStatus,
    BenchmarkDecision,
)
from athena.evaluation.quality_gate import (
    QualityGateResult,
    QualityGateStatus,
)


class QualityGateService:
    """Create final release quality decisions."""

    def evaluate(
        self,
        decision: BenchmarkDecision,
    ) -> QualityGateResult:
        """Convert benchmark decision into quality gate result."""

        if decision.status == BenchmarkDecisionStatus.PASS:
            return QualityGateResult(
                status=QualityGateStatus.PASS,
                message=("Benchmark quality maintained."),
                checks=[
                    "No regression detected.",
                ],
            )

        if decision.status == BenchmarkDecisionStatus.WARNING:
            return QualityGateResult(
                status=QualityGateStatus.WARNING,
                message=("Benchmark requires review."),
                checks=decision.reasons,
            )

        return QualityGateResult(
            status=QualityGateStatus.BLOCK,
            message=("Benchmark regression blocks release."),
            checks=decision.reasons,
        )
