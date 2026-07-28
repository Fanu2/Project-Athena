from __future__ import annotations

from collections.abc import Iterable

from athena.retrieval.query_intent import QueryIntent


class MetadataFilter:
    """Filters candidate documents using metadata from QueryIntent."""

    def filter(self, documents: Iterable, intent: QueryIntent):
        filtered = []

        for document in documents:
            language = getattr(document, "language", None)
            file_type = getattr(document, "file_type", None)

            if intent.languages and language not in intent.languages:
                continue

            if intent.file_types and file_type not in intent.file_types:
                continue

            filtered.append(document)

        return filtered

