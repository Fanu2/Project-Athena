"""
Project Athena

Retrieval Report Reporter.
"""

from __future__ import annotations

from athena.evaluation.retrieval_report import RetrievalReport


class RetrievalReportReporter:
    """Render RetrievalReport objects as Markdown."""

    def analyze(
        self,
        report: RetrievalReport,
    ) -> str:
        """Generate a Markdown retrieval intelligence report."""

        lines = [
            "# Retrieval Intelligence Report",
            "",
            "## Query",
            f"- Query: {report.query}",
            f"- Strategy: {report.strategy}",
            f"- Latency: {report.latency_ms:.2f} ms",
            f"- Candidates: {report.candidate_count}",
            "",
        ]

        if report.metadata:
            lines.extend(
                [
                    "## Environment",
                    "",
                ]
            )

            for key, value in sorted(report.metadata.items()):
                lines.append(f"- {key}: {value}")

            lines.append("")

        lines.extend(
            [
                "## Ranked Results",
                "",
            ]
        )

        for index, candidate in enumerate(report.results, start=1):
            lines.extend(
                [
                    f"### Rank {index}",
                    "",
                    f"**Document:** {candidate.title}",
                    "",
                    "| Signal | Score |",
                    "|-------|------:|",
                    f"| Final | {candidate.final_score:.3f} |",
                    f"| Semantic | {candidate.semantic_score:.3f} |",
                    f"| Keyword | {candidate.keyword_score:.3f} |",
                    f"| Metadata | {candidate.metadata_score:.3f} |",
                    f"| Identity | {candidate.identity_score:.3f} |",
                    "",
                    "**Explanation**",
                    "",
                    candidate.explanation or "_No explanation available._",
                    "",
                ]
            )

        return "\n".join(lines)

    def format(
        self,
        report: RetrievalReport,
    ) -> str:
        """Backward-compatible alias."""
        return self.analyze(report)
