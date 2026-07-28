"""
Retrieval analysis report generator.
"""

from __future__ import annotations

from athena.evaluation.retrieval_analysis import (
    RetrievalAnalysisReport,
)


class RetrievalAnalysisReporter:
    """Generate retrieval intelligence reports."""

    def analyze(
        self,
        report: RetrievalAnalysisReport,
    ) -> str:
        """Create markdown report."""

        lines: list[str] = []

        lines.append("# Athena Retrieval Intelligence Report")

        lines.append("")

        lines.append(f"Total findings: {report.total_findings}")

        lines.append("")

        if not report.findings:
            lines.append("No retrieval issues detected.")

            return "\n".join(lines)

        lines.append("## Findings")

        lines.append("")

        for finding in report.findings:
            lines.append(f"### {finding.question_id}")

            lines.append("")

            lines.append(f"- Issue: {finding.issue_type.value}")

            lines.append(f"- Expected: {finding.expected_document or 'unknown'}")

            lines.append(f"- Description: {finding.description}")

            lines.append("")

        return "\n".join(lines)

