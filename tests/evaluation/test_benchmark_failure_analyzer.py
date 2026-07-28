"""
Tests for benchmark failure analyzer.
"""

from athena.evaluation.benchmark_failure_analyzer import (
    BenchmarkFailureAnalyzer,
    FailureCategory,
)
from athena.evaluation.benchmark_models import (
    BenchmarkQuestion,
    BenchmarkRun,
)
from athena.evaluation.benchmark_session import (
    BenchmarkSession,
)


class FakeResult:
    """Minimal retrieval result."""

    def __init__(self, document_id: str) -> None:
        self.document_id = document_id


def test_correct_retrieval_classification() -> None:
    session = BenchmarkSession()

    session.runs.append(
        BenchmarkRun(
            question=BenchmarkQuestion(
                question_id="Q1",
                question="test",
                expected_document_id="doc1",
            ),
            retrieval_results=[
                FakeResult("doc1"),
            ],
        )
    )

    findings = BenchmarkFailureAnalyzer().analyze(session)

    assert len(findings) == 1
    assert findings[0].category == FailureCategory.CORRECT


def test_near_miss_classification() -> None:
    session = BenchmarkSession()

    session.runs.append(
        BenchmarkRun(
            question=BenchmarkQuestion(
                question_id="Q2",
                question="test",
                expected_document_id="doc1",
            ),
            retrieval_results=[
                FakeResult("doc2"),
                FakeResult("doc1"),
            ],
        )
    )

    findings = BenchmarkFailureAnalyzer().analyze(session)

    assert findings[0].category == FailureCategory.NEAR_MISS


def test_missing_classification() -> None:
    session = BenchmarkSession()

    session.runs.append(
        BenchmarkRun(
            question=BenchmarkQuestion(
                question_id="Q3",
                question="test",
                expected_document_id="doc1",
            ),
            retrieval_results=[
                FakeResult("doc2"),
            ],
        )
    )

    findings = BenchmarkFailureAnalyzer().analyze(session)

    assert findings[0].category == FailureCategory.MISSING

