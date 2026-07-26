"""
Tests for retrieval analysis models.
"""

from athena.evaluation.retrieval_analysis import (
    RetrievalAnalysisReport,
    RetrievalFinding,
    RetrievalIssueType,
)


def test_retrieval_finding_creation() -> None:
    """A retrieval finding should store evidence."""

    finding = RetrievalFinding(
        question_id="AQ-010",
        issue_type=RetrievalIssueType.NOT_RETRIEVED,
        expected_document="02-RETRIEVAL-MODEL.md",
        retrieved_documents=[
            "RIE-Specification-v1.0.docx",
        ],
        description="Expected document was not retrieved.",
    )

    assert finding.question_id == "AQ-010"
    assert (
        finding.issue_type
        == RetrievalIssueType.NOT_RETRIEVED
    )
    assert (
        finding.expected_document
        == "02-RETRIEVAL-MODEL.md"
    )


def test_retrieval_analysis_report_count() -> None:
    """Report should count findings."""

    findings = [
        RetrievalFinding(
            question_id="AQ-003",
            issue_type=(
                RetrievalIssueType.DUPLICATE_DOCUMENT
            ),
            expected_document="SAS-v1.0-Draft.md",
            retrieved_documents=[
                "SAS-v1.0-Draft.docx",
            ],
            description="Duplicate format selected.",
        ),
    ]

    report = RetrievalAnalysisReport(
        findings=findings,
    )

    assert report.total_findings == 1


def test_retrieval_issue_types_are_defined() -> None:
    """All required retrieval issue categories exist."""

    assert (
        RetrievalIssueType.DUPLICATE_DOCUMENT.value
        == "duplicate_document"
    )

    assert (
        RetrievalIssueType.WRONG_RANK.value
        == "wrong_rank"
    )

    assert (
        RetrievalIssueType.NOT_RETRIEVED.value
        == "not_retrieved"
    )
