"""
RAG context builder.

Builds LLM-ready context from retrieval results.
"""

from __future__ import annotations

from athena.ai.rag.models import (
    RAGContext,
    RAGSource,
)
from athena.ai.retrieval.models import SemanticResult


class ContextBuilder:
    """Build context for language models."""

    def build(
        self,
        question: str,
        results: list[SemanticResult],
    ) -> RAGContext:
        """Create RAG context."""

        context_parts: list[str] = []

        sources: list[RAGSource] = []

        for index, result in enumerate(
            results,
            start=1,
        ):
            context_parts.append(
                (
                    f"Source {index}\n"
                    f"Document: {result.document_id}\n"
                    f"Page: {result.page_number}\n"
                    f"{result.text}"
                )
            )

            sources.append(
                RAGSource(
                    chunk_id=result.chunk_id,
                    document_id=result.document_id,
                    page_number=result.page_number,
                    score=result.score,
                    text=result.text,
                )
            )

        context = "\n\n".join(
            context_parts,
        )

        return RAGContext(
            question=question,
            context=context,
            sources=sources,
        )
