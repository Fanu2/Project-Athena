"""
Evidence explanation generator.
"""

from __future__ import annotations


class EvidenceExplainer:
    """Generate human-readable retrieval explanations."""

    def explain(
        self,
        semantic_score: float,
        keyword_score: float,
        metadata_score: float,
        identity_score: float,
        document_authority_score: float,
    ) -> tuple[str, ...]:
        """Generate ranking reasons."""

        reasons: list[str] = []

        if semantic_score >= 0.7:
            reasons.append(
                "Strong semantic similarity"
            )

        if keyword_score >= 0.5:
            reasons.append(
                "Keyword match found"
            )

        if metadata_score >= 0.5:
            reasons.append(
                "Metadata match found"
            )

        if identity_score >= 0.5:
            reasons.append(
                "Query matched document identity"
            )

        if document_authority_score >= 0.5:
            reasons.append(
                "High document authority"
            )

        if not reasons:
            reasons.append(
                "Relevant semantic evidence retrieved"
            )

        return tuple(reasons)
