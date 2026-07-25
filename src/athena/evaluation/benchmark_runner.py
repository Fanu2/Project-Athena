"""
Benchmark runner.
"""

from __future__ import annotations

from athena.application.ai.retrieval_service import RetrievalService
from athena.domain.ai.question import Question

from athena.evaluation.benchmark_models import (
    BenchmarkMetrics,
    BenchmarkQuestion,
    BenchmarkRun,
)


class BenchmarkRunner:
    """Executes benchmark questions."""

    def __init__(
        self,
        retrieval_service: RetrievalService,
    ) -> None:
        self._retrieval_service = retrieval_service

    def run(
        self,
        question: BenchmarkQuestion,
    ) -> BenchmarkRun:
        """Execute one benchmark question."""

        retrieval_results = self._retrieval_service.retrieve(
            Question(text=question.question)
        )

        return BenchmarkRun(
            question=question,
            retrieval_results=retrieval_results,
            metrics=BenchmarkMetrics(),
        )
