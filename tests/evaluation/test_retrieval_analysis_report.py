"""
Tests for retrieval analysis report generator.
"""

from athena.evaluation.retrieval_analysis import (
    RetrievalAnalysisReport,
    RetrievalFinding,
    RetrievalIssueType,
)
from athena.evaluation.retrieval_analysis_report import (
    RetrievalAnalysisReporter,
)


def test_empty_report_generation() -> None:
    """Empty analysis should generate clean report."""

    reporter = RetrievalAnalysisReporter()

    report = RetrievalAnalysisReport(
        findings=[],
    )

    output = reporter.analyze(
        report,
    )

    assert (
        "# Athena Retrieval Intelligence Report"
        in output
    )

    assert (
        "Total findings: 0"
        in output
    )

    assert (
        "No retrieval issues detected."
        in output
    )


def test_finding_appears_in_report() -> None:
    """Findings should appear in markdown output."""

    reporter = RetrievalAnalysisReporter()

    finding = RetrievalFinding(
        question_id="AQ-010",
        issue_type=(
            RetrievalIssueType.NOT_RETRIEVED
        ),
        expected_document=(
            "02-RETRIEVAL-MODEL.md"
        ),
        retrieved_documents=[],
        description=(
            "Expected document was not retrieved."
        ),
    )

    report = RetrievalAnalysisReport(
        findings=[
            finding,
        ],
    )

    output = reporter.analyze(
        report,
    )

    assert "AQ-010" in output
    assert "not_retrieved" in output
    assert "02-RETRIEVAL-MODEL.md" in output


def test_finding_count_appears_in_report() -> None:
    """Report should contain finding count."""

    reporter = RetrievalAnalysisReporter()

    report = RetrievalAnalysisReport(
        findings=[
            RetrievalFinding(
                question_id="AQ-003",
                issue_type=(
                    RetrievalIssueType.WRONG_RANK
                ),
                expected_document=(
                    "SAS-v1.0-Draft.md"
                ),
                retrieved_documents=[
                    "SAS-v1.0-Draft.docx",
                ],
                description=(
                    "Expected document ranked lower."
                ),
            ),
        ],
    )

    output = reporter.analyze(
        report,
    )

    assert (
        "Total findings: 1"
        in output
    )

    assert (
        "wrong_rank"
        in output
    )

