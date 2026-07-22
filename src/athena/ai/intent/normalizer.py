"""
Query normalization for the Athena Intent Engine.

This module is responsible for converting raw user queries into a
canonical form suitable for intent detection. It performs only
normalization and intentionally contains no intent detection logic.
"""

from __future__ import annotations

import re
import unicodedata


class QueryNormalizer:
    """
    Normalizes user queries before intent detection.

    Responsibilities
    ----------------
    - Normalize Unicode text
    - Convert to lowercase
    - Collapse repeated whitespace
    - Remove unnecessary punctuation
    - Preserve the semantic meaning of the query

    This class does NOT:
    - Detect intents
    - Replace synonyms
    - Stem or lemmatize words
    - Perform keyword matching
    """

    _WHITESPACE_PATTERN = re.compile(r"\s+")
    _PUNCTUATION_PATTERN = re.compile(r"[^\w\s]")

    def normalize(self, query: str) -> str:
        """
        Normalize a user query.

        Parameters
        ----------
        query : str
            Raw user input.

        Returns
        -------
        str
            Canonical normalized query.
        """
        if not query:
            return ""

        query = self._normalize_unicode(query)
        query = self._normalize_case(query)
        query = self._normalize_punctuation(query)
        query = self._normalize_whitespace(query)

        return query

    @staticmethod
    def _normalize_unicode(text: str) -> str:
        """Normalize Unicode characters."""
        return unicodedata.normalize("NFKC", text)

    @staticmethod
    def _normalize_case(text: str) -> str:
        """Convert text to lowercase."""
        return text.lower()

    def _normalize_whitespace(self, text: str) -> str:
        """Collapse repeated whitespace into a single space."""
        return self._WHITESPACE_PATTERN.sub(" ", text).strip()

    def _normalize_punctuation(self, text: str) -> str:
        """
        Remove punctuation while preserving letters, digits,
        underscores and whitespace.
        """
        return self._PUNCTUATION_PATTERN.sub("", text)