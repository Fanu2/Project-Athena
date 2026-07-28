"""
Keyword retrieval adapter.
"""

from __future__ import annotations

from athena.ai.retrieval.models import SemanticResult
from athena.indexing.models import DocumentChunk


class KeywordAdapter:
    """Convert keyword matches into retrieval results."""

    def convert(
        self,
        chunks: list[DocumentChunk],
        query: str,
    ) -> list[SemanticResult]:
        """Convert keyword matches to SemanticResult objects."""

        results: list[SemanticResult] = []

        query_terms = {
            term.lower()
            for term in query.split()
            if term.strip()
        }

        for chunk in chunks:
            text = chunk.text.lower()

            matched_terms = sum(
                1
                for term in query_terms
                if term in text
            )

            if not query_terms:
                score = 0.0
            else:
                score = (
                    matched_terms
                    / len(query_terms)
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
                )
            )

        results.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        return results

