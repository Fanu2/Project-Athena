"""
Retrieval diagnostic analyzer.
"""

from __future__ import annotations

from pathlib import Path

from athena.evaluation.retrieval_analysis import (
    RetrievalAnalysisReport,
    RetrievalFinding,
    RetrievalIssueType,
)


class RetrievalDiagnosticAnalyzer:
    """Analyze benchmark diagnostics."""

    def analyze(
        self,
        path: str | Path,
    ) -> RetrievalAnalysisReport:
        """Create retrieval findings from diagnostics."""

        content = Path(path).read_text(
            encoding="utf-8",
        )

        findings: list[RetrievalFinding] = []

        blocks = content.split(
            "## Question ",
        )

        for block in blocks[1:]:
            lines = block.splitlines()

            question_id = lines[0].strip()

            if "Status: Not Retrieved" in block:
                findings.append(
                    RetrievalFinding(
                        question_id=question_id,
                        issue_type=(RetrievalIssueType.NOT_RETRIEVED),
                        expected_document="",
                        retrieved_documents=[],
                        description=("Expected document was not retrieved."),
                    )
                )

            elif "Expected document retrieved at rank" in block:
                findings.append(
                    RetrievalFinding(
                        question_id=question_id,
                        issue_type=(RetrievalIssueType.WRONG_RANK),
                        expected_document="",
                        retrieved_documents=[],
                        description=("Expected document was not ranked first."),
                    )
                )

        return RetrievalAnalysisReport(
            findings=findings,
        )
