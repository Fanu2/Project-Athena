"""
Benchmark runner.
"""

from __future__ import annotations

from time import perf_counter

from athena.application.ai.retrieval_service import RetrievalService
from athena.domain.ai.question import Question

from athena.evaluation.benchmark_models import (
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

        start = perf_counter()

        retrieval_results = self._retrieval_service.retrieve(
            Question(text=question.question)
        )

        elapsed_ms = (perf_counter() - start) * 1000.0

        return BenchmarkRun(
            question=question,
            retrieval_results=retrieval_results,
            elapsed_ms=elapsed_ms,
        )
