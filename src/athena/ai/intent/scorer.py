"""
Intent scoring for the Athena Intent Engine.

This module converts matched intent keywords into numerical scores.
It performs no confidence calculation or final intent selection.
"""

from __future__ import annotations

from collections import defaultdict

from .models import IntentType, MatchedIntent


class IntentScorer:
    """
    Scores matched intents based on keyword occurrences.
    """

    def score(
        self,
        matches: tuple[MatchedIntent, ...],
    ) -> dict[IntentType, int]:
        """
        Compute raw scores for each detected intent.

        Parameters
        ----------
        matches
            Tuple of matched intent keywords.

        Returns
        -------
        dict[IntentType, int]
            Raw score for every detected intent.
        """
        scores: dict[IntentType, int] = defaultdict(int)

        for match in matches:
            scores[match.intent] += match.occurrences

        return dict(scores)