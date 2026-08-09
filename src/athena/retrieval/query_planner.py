"""
Query planning and intent extraction.
"""

from __future__ import annotations

from athena.retrieval.query_filters import (
    FILE_TYPES,
    LANGUAGES,
    OPERATIONS,
)
from athena.retrieval.query_intent import (
    QueryIntent,
)


class QueryPlanner:
    """
    Parses user queries into structured retrieval intent.
    """

    def parse(
        self,
        query: str,
    ) -> QueryIntent:
        """Convert query into retrieval intent."""

        words = query.lower().split()

        operation = next(
            (
                word
                for word in words
                if word in OPERATIONS
            ),
            "search",
        )

        languages = tuple(
            language.title()
            for language in sorted(LANGUAGES)
            if language in words
        )

        file_types = tuple(
            file_type
            for file_type in sorted(FILE_TYPES)
            if file_type in words
        )

        entities = self._extract_entities(
            words,
        )

        strategy = self._select_strategy(
            words,
        )

        ranking_profile = (
            self._select_ranking_profile(
                words,
            )
        )

        confidence = (
            self._calculate_confidence(
                strategy,
                ranking_profile,
            )
        )

        return QueryIntent(
            original_query=query,
            # Preserve existing retrieval contract.
            semantic_query=operation,
            languages=languages,
            file_types=file_types,
            entities=entities,
            strategy=strategy,
            ranking_profile=ranking_profile,
            confidence=confidence,
        )

    def _select_strategy(
        self,
        words: list[str],
    ) -> str:
        """Select retrieval strategy."""

        exact_terms = {
            "exact",
            "phrase",
            "code",
            "number",
            "id",
        }

        if any(
            word in exact_terms
            for word in words
        ):
            return "keyword"

        metadata_terms = {
            "owner",
            "ownership",
            "date",
            "author",
            "property",
            "document",
        }

        if any(
            word in metadata_terms
            for word in words
        ):
            return "metadata"

        return "hybrid"

    def _select_ranking_profile(
        self,
        words: list[str],
    ) -> str:
        """Select ranking profile."""

        legal_terms = {
            "ownership",
            "khasra",
            "khewat",
            "jamabandi",
            "revenue",
            "deed",
        }

        if any(
            word in legal_terms
            for word in words
        ):
            return "legal_document"

        technical_terms = {
            "architecture",
            "software",
            "code",
            "system",
        }

        if any(
            word in technical_terms
            for word in words
        ):
            return "technical"

        return "default"

    def _extract_entities(
        self,
        words: list[str],
    ) -> tuple[str, ...]:
        """Extract simple query entities."""

        ignored = (
            OPERATIONS
            | LANGUAGES
            | FILE_TYPES
        )

        return tuple(
            word
            for word in words
            if word not in ignored
            and len(word) > 2
        )

    def _calculate_confidence(
        self,
        strategy: str,
        ranking_profile: str,
    ) -> float:
        """Estimate planner confidence."""

        confidence = 0.5

        if strategy != "hybrid":
            confidence += 0.2

        if ranking_profile != "default":
            confidence += 0.2

        return min(
            confidence,
            1.0,
        )
