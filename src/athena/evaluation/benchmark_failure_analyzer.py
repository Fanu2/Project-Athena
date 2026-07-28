"""
Benchmark failure analyzer.

Classifies retrieval benchmark outcomes.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from athena.evaluation.benchmark_session import BenchmarkSession


class FailureCategory(str, Enum):
    """Benchmark outcome classification."""

    CORRECT = "correct"
    NEAR_MISS = "near_miss"
    MISSING = "missing"
    DUPLICATE_COMPETITION = "duplicate_competition"


@dataclass(slots=True)
class BenchmarkFinding:
    """One benchmark diagnostic finding."""

    question_id: str
    category: FailureCategory
    expected_document: str | None
    retrieved_documents: list[str]


class BenchmarkFailureAnalyzer:
    """Analyze benchmark retrieval outcomes."""

    def analyze(
        self,
        session: BenchmarkSession,
    ) -> list[BenchmarkFinding]:
        """Classify benchmark runs."""

        findings: list[BenchmarkFinding] = []

        for run in session.runs:
            expected = run.question.expected_document_id

            documents = [result.document_id for result in run.retrieval_results]

            if expected is None:
                continue

            if documents and documents[0] == expected:
                category = FailureCategory.CORRECT

            elif expected in documents[:5]:
                category = FailureCategory.NEAR_MISS

            else:
                category = FailureCategory.MISSING

            findings.append(
                BenchmarkFinding(
                    question_id=run.question.question_id,
                    category=category,
                    expected_document=expected,
                    retrieved_documents=documents,
                )
            )

        return findings

