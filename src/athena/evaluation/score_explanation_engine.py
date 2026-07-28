"""
Project Athena

Score Explanation Engine.

Generates human-readable explanations describing why a retrieval
candidate received its ranking.
"""


class ScoreExplanationEngine:
    """Generates explanations for retrieval candidate scores."""

    def explain(self, candidate) -> list[str]:
        """
        Build a list of explanations for a retrieval candidate.

        Parameters
        ----------
        candidate
            Any object exposing semantic_score, keyword_score,
            metadata_score, and identity_score attributes.

        Returns
        -------
        list[str]
            Human-readable explanation strings.
        """

        explanations: list[str] = []

        semantic_score = getattr(candidate, "semantic_score", 0.0)
        keyword_score = getattr(candidate, "keyword_score", 0.0)
        metadata_score = getattr(candidate, "metadata_score", 0.0)
        identity_score = getattr(candidate, "identity_score", 0.0)

        if semantic_score > 0:
            explanations.append(
                f"High semantic similarity ({semantic_score:.2f})"
            )

        if keyword_score > 0:
            explanations.append(
                f"Strong keyword relevance ({keyword_score:.2f})"
            )

        if metadata_score > 0:
            explanations.append(
                f"Metadata match ({metadata_score:.2f})"
            )

        if identity_score > 0:
            explanations.append(
                f"Identity-aware boost ({identity_score:.2f})"
            )

        if not explanations:
            explanations.append("No significant ranking signals detected.")

        return explanations

