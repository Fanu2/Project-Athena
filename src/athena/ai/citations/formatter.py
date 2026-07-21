"""
Citation formatter.
"""

from __future__ import annotations

from athena.ai.citations.models import Citation


class CitationFormatter:
    """Formats citations for display."""

    @staticmethod
    def format(citation: Citation) -> str:
        """
        Format a citation for display.
        """

        return (
            f"{citation.title}\n"
            f"Page {citation.page_number}\n"
            f"Characters {citation.start_offset}"
            f"–{citation.end_offset}\n"
            f"Similarity {citation.score:.2f}"
        )
