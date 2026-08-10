"""
Keyword retrieval adapter.
"""

from __future__ import annotations

import re
import unicodedata

from athena.ai.retrieval.models import SemanticResult
from athena.indexing.models import DocumentChunk


class KeywordAdapter:
    """Convert keyword matches into retrieval results."""

    @staticmethod
    def _normalize_text(
        text: str,
    ) -> str:
        """
        Normalize multilingual text.

        Handles:
        - Unicode normalization
        - punctuation
        - whitespace
        """

        value = unicodedata.normalize(
            "NFC",
            text,
        )

        value = value.lower()

        value = re.sub(
            r"[^\w\s\u0900-\u097F\u0980-\u09FF\u0A00-\u0A7F\u0F00-\u0FFF]",
            " ",
            value,
        )

        value = re.sub(
            r"\s+",
            " ",
            value,
        )

        return value.strip()

    @classmethod
    def _tokenize(
        cls,
        text: str,
    ) -> set[str]:
        """
        Convert text into normalized tokens.
        """

        tokens = {
            token
            for token in cls._normalize_text(
                text,
            ).split()
            if len(token) > 1
        }

        return tokens

    def convert(
        self,
        chunks: list[DocumentChunk],
        query: str,
    ) -> list[SemanticResult]:
        """
        Convert keyword matches into retrieval results.
        """

        results: list[SemanticResult] = []

        query_terms = self._tokenize(
            query,
        )

        for chunk in chunks:

            document_terms = self._tokenize(
                chunk.text,
            )

            matched_terms = (
                query_terms
                &
                document_terms
            )

            if not query_terms:
                score = 0.0
            else:
                score = (
                    len(matched_terms)
                    /
                    len(query_terms)
                )

            results.append(
                SemanticResult(
                    chunk_id=chunk.chunk_id,
                    document_id=chunk.document_id,
                    document_name=chunk.document_id,
                    document_title=(
                        chunk.heading
                        or chunk.document_id
                    ),
                    page_number=chunk.page_number,
                    start_offset=chunk.start_offset,
                    end_offset=chunk.end_offset,
                    text=chunk.text,
                    score=score,
                    keyword_score=score,
                )
            )

        results.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        return results
