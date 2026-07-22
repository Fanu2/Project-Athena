"""
Pattern matching for the Athena Intent Engine.

This module is responsible for identifying which intent patterns
appear in a normalized user query.

Responsibilities
----------------
- Match keywords against a normalized query.
- Count keyword occurrences.
- Return structured matches.

This module does NOT:
- Rank intents.
- Calculate confidence.
- Choose the winning intent.
"""

from __future__ import annotations

import re

from .models import MatchedIntent
from .patterns import INTENT_PATTERNS


class PatternMatcher:
    """
    Matches normalized user queries against intent patterns.
    """

    def match(self, query: str) -> tuple[MatchedIntent, ...]:
        """
        Match all known intent keywords within a normalized query.

        Parameters
        ----------
        query : str
            Normalized user query.

        Returns
        -------
        tuple[MatchedIntent, ...]
            All detected intent matches.
        """
        if not query:
            return ()

        matches: list[MatchedIntent] = []

        for intent, keywords in INTENT_PATTERNS.items():
            for keyword in keywords:
                count = self._count_keyword(query, keyword)

                if count > 0:
                    matches.append(
                        MatchedIntent(
                            intent=intent,
                            keyword=keyword,
                            occurrences=count,
                        )
                    )

        return tuple(matches)

    @staticmethod
    def _count_keyword(query: str, keyword: str) -> int:
        """
        Count whole-word occurrences of a keyword.

        Parameters
        ----------
        query : str
            Normalized query.

        keyword : str
            Keyword to search for.

        Returns
        -------
        int
            Number of occurrences.
        """
        pattern = rf"\b{re.escape(keyword)}\b"
        return len(re.findall(pattern, query))