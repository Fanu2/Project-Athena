"""
Intent detection pipeline for the Athena Intent Engine.
"""

from __future__ import annotations

from .confidence import ConfidenceCalculator
from .matcher import PatternMatcher
from .models import IntentResult
from .normalizer import QueryNormalizer
from .scorer import IntentScorer


class IntentDetector:
    """
    Coordinates the complete intent detection pipeline.
    """

    def __init__(self) -> None:
        self._normalizer = QueryNormalizer()
        self._matcher = PatternMatcher()
        self._scorer = IntentScorer()
        self._confidence = ConfidenceCalculator()

    def detect(self, query: str) -> IntentResult:
        """
        Detect the user's intent.

        Parameters
        ----------
        query
            Raw user query.

        Returns
        -------
        IntentResult
            Final intent detection result.
        """
        normalized_query = self._normalizer.normalize(query)

        matches = self._matcher.match(normalized_query)

        scores = self._scorer.score(matches)

        result = self._confidence.calculate(scores)

        return IntentResult(
            intent=result.intent,
            confidence=result.confidence,
            matched_keywords=tuple(
                match.keyword
                for match in matches
            ),
            normalized_query=normalized_query,
        )