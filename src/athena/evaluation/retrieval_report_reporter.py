"""
Project Athena

Retrieval Report Formatter.
"""

from athena.evaluation.retrieval_report import RetrievalReport


class RetrievalReportReporter:
    """Formats RetrievalReport objects as readable text."""

    def format(self, report: RetrievalReport) -> str:

        lines = [
            "Retrieval Intelligence Report",
            "=" * 30,
            f"Query: {report.query}",
            f"Strategy: {report.strategy}",
            f"Latency: {report.latency_ms:.2f} ms",
            f"Candidates: {report.candidate_count}",
            "",
        ]

        for index, candidate in enumerate(report.results, start=1):

            lines.extend(
                [
                    f"{index}. {candidate.title}",
                    f"   Final Score : {candidate.final_score:.3f}",
                    f"   Semantic    : {candidate.semantic_score:.3f}",
                    f"   Keyword     : {candidate.keyword_score:.3f}",
                    f"   Metadata    : {candidate.metadata_score:.3f}",
                    f"   Identity    : {candidate.identity_score:.3f}",
                    f"   Explanation : {candidate.explanation}",
                    "",
                ]
            )

        return "\n".join(lines)

