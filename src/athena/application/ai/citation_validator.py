"""
Citation validation service.
"""

from __future__ import annotations

from athena.domain.ai.citation import Citation


class CitationValidator:
    """Validate citation integrity."""

    def validate(
        self,
        citation: Citation,
    ) -> bool:
        """Check citation fields."""

        if not citation.document_name:
            return False

        if citation.page < 0:
            return False

        if not citation.snippet.strip():
            return False

        if citation.score < 0:
            return False

        return True
