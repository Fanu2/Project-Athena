"""
RAG context builder.

Builds LLM-ready context from retrieval results.
"""

from __future__ import annotations

from pathlib import Path

from athena.ai.rag.models import (
    RAGContext,
    RAGSource,
)
from athena.ai.retrieval.models import SemanticResult
from athena.documents.service import DocumentService


class ContextBuilder:
    """Build context for language models."""

    def __init__(
        self,
        document_service: DocumentService | None = None,
    ) -> None:
        """Initialize context builder."""

        self._document_service = document_service

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
            document_name = result.document_id
            document_path = Path()

            if self._document_service is not None:
                document = self._document_service.get_document(
                    result.document_id,
                )

                if document is not None:
                    document_name = document.name
                    document_path = document.path

            context_parts.append(
                (
                    f"Source {index}\n"
                    f"Document: {document_name}\n"
                    f"Page: {result.page_number}\n"
                    f"{result.text}"
                )
            )

            sources.append(
                RAGSource(
                    chunk_id=result.chunk_id,
                    document_id=result.document_id,
                    document_name=document_name,
                    document_path=document_path,
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
