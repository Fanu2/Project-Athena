"""
Unit tests for BenchmarkMetricsEngine.
"""

from __future__ import annotations

from uuid import uuid4

from athena.domain.ai.retrieval_result import RetrievalResult

from athena.evaluation.benchmark_metrics_engine import BenchmarkMetricsEngine
from athena.evaluation.benchmark_models import (
    BenchmarkQuestion,
    BenchmarkRun,
)
from athena.evaluation.benchmark_session import BenchmarkSession


def test_empty_session_returns_zero_summary():
    """Empty benchmark session should produce zero metrics."""

    engine = BenchmarkMetricsEngine()
    session = BenchmarkSession()

    summary = engine.summarize(session)

    assert summary.total_questions == 0
    assert summary.successful_retrievals == 0
    assert summary.failed_retrievals == 0
    assert summary.top1_accuracy == 0.0
    assert summary.top3_accuracy == 0.0
    assert summary.top5_accuracy == 0.0
    assert summary.mean_reciprocal_rank == 0.0
    assert summary.average_latency_ms == 0.0
    assert summary.median_latency_ms == 0.0
    assert summary.fastest_latency_ms == 0.0
    assert summary.slowest_latency_ms == 0.0


def test_summary_returns_benchmark_summary():
    """Engine should always return a BenchmarkSummary."""

    engine = BenchmarkMetricsEngine()
    session = BenchmarkSession()

    summary = engine.summarize(session)

    assert summary is not None


def test_empty_session_has_no_runs():
    """Sanity check for BenchmarkSession."""

    session = BenchmarkSession()

    assert session.total_questions == 0
    assert len(session.runs) == 0


def test_question_model_can_be_created():
    """BenchmarkQuestion should construct successfully."""

    question = BenchmarkQuestion(
        question_id="Q1",
        question="What is Athena?",
    )

    assert question.question_id == "Q1"
    assert question.question == "What is Athena?"


def test_success_failure_counts():
    """Engine should correctly count successful and failed retrievals."""

    engine = BenchmarkMetricsEngine()

    session = BenchmarkSession()

    question = BenchmarkQuestion(
        question_id="Q1",
        question="Athena",
    )

    success_run = BenchmarkRun(
        question=question,
        retrieval_results=[
            RetrievalResult(
                document_id=uuid4(),
                document_name="doc1",
                page=1,
                text="Athena",
                score=0.95,
            )
        ],
        elapsed_ms=12.0,
    )

    failed_run = BenchmarkRun(
        question=question,
        retrieval_results=[],
        elapsed_ms=18.0,
    )

    session.runs.extend([success_run, failed_run])

    summary = engine.summarize(session)

    assert summary.total_questions == 2
    assert summary.successful_retrievals == 1
    assert summary.failed_retrievals == 1


def test_latency_statistics():
    """Engine should calculate latency statistics."""

    engine = BenchmarkMetricsEngine()

    session = BenchmarkSession()

    question = BenchmarkQuestion(
        question_id="Q1",
        question="Athena",
    )

    for latency in (10.0, 20.0, 30.0):
        session.runs.append(
            BenchmarkRun(
                question=question,
                retrieval_results=[],
                elapsed_ms=latency,
            )
        )

    summary = engine.summarize(session)

    assert summary.average_latency_ms == 20.0
    assert summary.median_latency_ms == 20.0
    assert summary.fastest_latency_ms == 10.0
    assert summary.slowest_latency_ms == 30.0


def test_top1_accuracy():

    doc = uuid4()

    question = BenchmarkQuestion(
        question_id="Q1",
        question="Question",
        expected_document_id=str(doc),
    )

    run = BenchmarkRun(
        question=question,
        retrieval_results=[
            RetrievalResult(
                document_id=doc,
                document_name="Doc",
                page=1,
                text="Answer",
                score=0.95,
            )
        ],
        elapsed_ms=10,
    )

    session = BenchmarkSession(
        runs=[run],
    )

    summary = BenchmarkMetricsEngine().summarize(
        session,
    )

    assert summary.top1_accuracy == 1.0
    assert summary.top3_accuracy == 1.0
    assert summary.top5_accuracy == 1.0
    assert summary.mean_reciprocal_rank == 1.0


def test_mrr_rank_two():

    expected = uuid4()

    run = BenchmarkRun(
        question=BenchmarkQuestion(
            question_id="Q1",
            question="Question",
            expected_document_id=str(expected),
        ),
        retrieval_results=[
            RetrievalResult(
                uuid4(),
                "Wrong",
                1,
                "",
                0.99,
            ),
            RetrievalResult(
                expected,
                "Correct",
                1,
                "",
                0.90,
            ),
        ],
        elapsed_ms=5,
    )

    session = BenchmarkSession(
        runs=[run],
    )

    summary = BenchmarkMetricsEngine().summarize(
        session,
    )

    assert summary.top1_accuracy == 0.0
    assert summary.top3_accuracy == 1.0
    assert summary.top5_accuracy == 1.0
    assert summary.mean_reciprocal_rank == 0.5


def test_document_not_found():

    run = BenchmarkRun(
        question=BenchmarkQuestion(
            question_id="Q1",
            question="Question",
            expected_document_id=str(uuid4()),
        ),
        retrieval_results=[
            RetrievalResult(
                uuid4(),
                "Wrong",
                1,
                "",
                0.8,
            ),
        ],
        elapsed_ms=5,
    )

    session = BenchmarkSession(
        runs=[run],
    )

    summary = BenchmarkMetricsEngine().summarize(
        session,
    )

    assert summary.top1_accuracy == 0.0
    assert summary.top3_accuracy == 0.0
    assert summary.top5_accuracy == 0.0
    assert summary.mean_reciprocal_rank == 0.0
