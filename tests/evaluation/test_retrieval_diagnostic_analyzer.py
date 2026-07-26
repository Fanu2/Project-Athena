"""
Tests for retrieval diagnostic analyzer.
"""

from pathlib import Path

from athena.evaluation.retrieval_diagnostic_analyzer import (
    RetrievalDiagnosticAnalyzer,
)
from athena.evaluation.retrieval_analysis import (
    RetrievalIssueType,
)


def test_analyzer_detects_not_retrieved(
    tmp_path: Path,
) -> None:
    """Analyzer should detect missing retrieval."""

    diagnostic = """
## Question AQ-010

- Expected Document: 02-RETRIEVAL-MODEL.md
- Status: Not Retrieved

### Notes

- Expected document was not retrieved.
"""

    file = tmp_path / "benchmark_diagnostics.md"

    file.write_text(
        diagnostic,
        encoding="utf-8",
    )

    analyzer = RetrievalDiagnosticAnalyzer()

    report = analyzer.analyze(
        file,
    )

    assert report.total_findings == 1

    assert (
        report.findings[0].issue_type
        == RetrievalIssueType.NOT_RETRIEVED
    )


def test_analyzer_detects_wrong_rank(
    tmp_path: Path,
) -> None:
    """Analyzer should detect non-first ranking."""

    diagnostic = """
## Question AQ-003

- Expected Document: SAS-v1.0-Draft.md
- Status: Found
- Rank: 2

### Notes

- Expected document retrieved at rank 2.
"""

    file = tmp_path / "benchmark_diagnostics.md"

    file.write_text(
        diagnostic,
        encoding="utf-8",
    )

    analyzer = RetrievalDiagnosticAnalyzer()

    report = analyzer.analyze(
        file,
    )

    assert report.total_findings == 1

    assert (
        report.findings[0].issue_type
        == RetrievalIssueType.WRONG_RANK
    )


def test_analyzer_empty_when_no_issues(
    tmp_path: Path,
) -> None:
    """Analyzer should return empty report."""

    diagnostic = """
## Question AQ-001

- Expected Document: constitution.md
- Status: Found
- Rank: 1

### Notes

- Expected document ranked first.
"""

    file = tmp_path / "benchmark_diagnostics.md"

    file.write_text(
        diagnostic,
        encoding="utf-8",
    )

    analyzer = RetrievalDiagnosticAnalyzer()

    report = analyzer.analyze(
        file,
    )

    assert report.total_findings == 0
