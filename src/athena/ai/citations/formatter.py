"""
Citation formatter.
"""

from __future__ import annotations

from athena.ai.rag.models import RAGSource


class CitationFormatter:
    """Formats RAG sources for presentation."""

    @staticmethod
    def format(source: RAGSource) -> str:
        """Format a RAG source for display."""

        return (
            f"{source.document_name}\n"
            f"Page {source.page_number}\n"
            f"Similarity {source.score:.2f}"
        )
