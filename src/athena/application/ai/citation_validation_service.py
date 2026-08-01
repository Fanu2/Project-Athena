"""
Citation validation service.
"""

from __future__ import annotations

from athena.domain.ai.citation import Citation
from athena.domain.ai.citation_validation import CitationValidation


class CitationValidationService:
    """Validate citation support."""

    def validate(
        self,
        citation: Citation,
    ) -> CitationValidation:
        """
        Validate a citation.

        Current implementation validates
        evidence completeness.
        """

        reasons = []

        supported = True

        if not citation.snippet.strip():
            supported = False

            reasons.append(
                "Missing supporting text",
            )
        else:
            reasons.append(
                "Supporting text available",
            )

        if citation.score <= 0:
            supported = False

            reasons.append(
                "Invalid relevance score",
            )

        else:
            reasons.append(
                "Positive relevance score",
            )

        confidence = (
            citation.score
            if supported
            else 0.0
        )

        return CitationValidation(
            supported=supported,
            confidence=confidence,
            reasons=tuple(reasons),
        )