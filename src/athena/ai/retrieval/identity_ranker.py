"""
Document identity ranking.

Provides a score indicating how closely a query
matches a document identity (name/title) and
basic code intent.
"""

from __future__ import annotations

import re
from pathlib import Path


class IdentityRanker:
    """Calculate document identity relevance."""

    @staticmethod
    def _normalize(value: str) -> str:
        """Normalize names for comparison."""

        value = Path(
            value,
        ).name.lower().strip()

        value = re.sub(
            r"\.[a-z0-9]+$",
            "",
            value,
        )

        value = value.replace(
            "_",
            "-",
        )

        value = re.sub(
            r"^\d+-",
            "",
            value,
        )

        return value.strip("-")

    def _code_intent_score(
        self,
        query: str,
        document_name: str,
    ) -> float:
        """Weak code-aware identity signal."""

        query = query.lower()

        document = self._normalize(
            document_name,
        )

        # Storage/repository intent has priority
        if (
            "storage" in query
            or "stored" in query
            or "repository" in query
        ):
            if document == "repository":
                return 0.8

            if document == "storage":
                return 0.6

            return 0.0

        # General implementation intent
        if (
            "implemented" in query
            or "implementation" in query
            or "defined" in query
        ):
            if document == "service":
                return 0.7

            if document == "engine":
                return 0.6

            if document == "application-context":
                return 0.1

        return 0.0
    def score(
        self,
        query: str,
        document_name: str,
        document_title: str | None = None,
    ) -> float:
        """Calculate identity match score."""

        query_value = self._normalize(
            query,
        )

        names = [
            self._normalize(document_name),
        ]

        if document_title:
            names.append(
                self._normalize(document_title),
            )

        for name in names:
            if query_value == name:
                return 1.0

            if query_value in name or name in query_value:
                return 0.5

        return self._code_intent_score(
            query,
            document_name,
        )
