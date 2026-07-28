from __future__ import annotations

from athena.retrieval.query_filters import (
    FILE_TYPES,
    LANGUAGES,
    OPERATIONS,
)
from athena.retrieval.query_intent import QueryIntent


class QueryPlanner:
    """Parses a user query into a structured QueryIntent."""

    def parse(self, query: str) -> QueryIntent:
        words = query.lower().split()

        operation = next(
            (word for word in words if word in OPERATIONS),
            query.lower(),
        )

        languages = tuple(language.title() for language in sorted(LANGUAGES) if language in words)

        file_types = tuple(file_type for file_type in sorted(FILE_TYPES) if file_type in words)

        return QueryIntent(
            original_query=query,
            semantic_query=operation,
            languages=languages,
            file_types=file_types,
        )

