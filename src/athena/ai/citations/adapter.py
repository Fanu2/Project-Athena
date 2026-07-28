"""
Citation adapter.
"""

from __future__ import annotations

from athena.ai.citations import Citation
from athena.ai.rag.models import RAGSource
from athena.ai.retrieval.models import SemanticResult


class CitationAdapter:
    """Converts retrieval objects into Citation models."""

    @staticmethod
    def from_semantic_result(
        result: SemanticResult,
    ) -> Citation:

        return Citation(
            document_id=result.document_id,
            title=result.document_title,
            page_number=result.page_number,
            start_offset=result.start_offset,
            end_offset=result.end_offset,
            score=result.score,
        )

    @staticmethod
    def from_rag_source(
        source: RAGSource,
    ) -> Citation:

        return Citation(
            document_id=source.document_id,
            title=source.document_name,
            page_number=source.page_number,
            start_offset=0,
            end_offset=len(source.text),
            score=source.score,
        )
