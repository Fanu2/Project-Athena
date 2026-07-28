"""
Evaluation quality gate facade.
"""

from __future__ import annotations

from athena.evaluation.benchmark_decision import (
    BenchmarkDecision,
)
from athena.evaluation.quality_gate import (
    QualityGateResult,
)
from athena.evaluation.quality_gate_service import (
    QualityGateService,
)


class EvaluationGate:
    """Run Athena evaluation quality checks."""

    def __init__(self) -> None:
        self._service = QualityGateService()

    def evaluate(
        self,
        decision: BenchmarkDecision,
    ) -> QualityGateResult:
        """Evaluate release readiness."""

        return self._service.evaluate(
            decision,
        )

