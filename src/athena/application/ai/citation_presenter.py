"""
Citation presenter.
"""

from __future__ import annotations

from athena.application.ai.citation_view import CitationView
from athena.domain.ai.citation import Citation


class CitationPresenter:
    """Convert citations into presentation models."""

    def present(
        self,
        citations: list[Citation],
    ) -> list[CitationView]:
        """Prepare citations for display."""

        return [
            CitationView(
                document_name=citation.document_name,
                page=citation.page,
                snippet=citation.snippet,
                score=citation.score,
                ranking_reasons=citation.ranking_reasons,
            )
            for citation in citations
        ]
