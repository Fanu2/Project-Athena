"""
Document matcher.
"""

from __future__ import annotations

from pathlib import Path

from .models import DocumentReference


class MetadataMatcher:
    """
    Match document titles mentioned in a query.
    """

    def __init__(
        self,
        document_titles: tuple[str, ...],
    ) -> None:
        self._document_titles = document_titles

    @staticmethod
    def _normalize(text: str) -> str:
        """
        Normalize text for comparison.
        """
        return " ".join(text.casefold().split())

    @staticmethod
    def _title_without_extension(title: str) -> str:
        """
        Remove the filename extension.
        """
        return Path(title).stem

    def match(
        self,
        query: str,
    ) -> tuple[DocumentReference, ...]:
        """
        Return matching documents.
        """
        normalized_query = self._normalize(query)

        matches: list[DocumentReference] = []

        for title in self._document_titles:
            normalized_title = self._normalize(
                self._title_without_extension(title)
            )

            if normalized_title and normalized_title in normalized_query:
                matches.append(
                    DocumentReference(
                        document_id=title,
                        title=title,
                        confidence=1.0,
                    )
                )

        return tuple(matches)