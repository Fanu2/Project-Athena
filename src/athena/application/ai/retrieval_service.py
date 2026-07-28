"""
Retrieval service.
"""

from __future__ import annotations

from athena.ai.retrieval.service import (
    RetrievalService as SemanticRetrievalService,
)
from athena.domain.ai.question import Question
from athena.domain.ai.retrieval_result import RetrievalResult


class RetrievalService:
    """Retrieve relevant evidence for a question."""

    def __init__(
        self,
        semantic_retrieval_service: SemanticRetrievalService,
    ) -> None:
        self._semantic_retrieval_service = semantic_retrieval_service

    @property
    def semantic_retrieval_service(
        self,
    ) -> SemanticRetrievalService:
        """Return the underlying semantic retrieval service."""

        return self._semantic_retrieval_service

    def retrieve(
        self,
        question: Question,
    ) -> list[RetrievalResult]:
        """
        Retrieve evidence supporting the supplied question.
        """

        semantic_results = self._semantic_retrieval_service.search_similar(
            query=question.text,
        )

        results: list[RetrievalResult] = []

        for item in semantic_results:
            results.append(
                RetrievalResult(
                    document_id=item.document_id,
                    document_name=item.document_name,
                    page=item.page_number,
                    text=item.text,
                    score=item.score,
                    semantic_score=getattr(
                        item,
                        "semantic_score",
                        item.score,
                    ),
                    keyword_score=getattr(
                        item,
                        "keyword_score",
                        0.0,
                    ),
                    metadata_score=getattr(
                        item,
                        "metadata_score",
                        0.0,
                    ),
                    identity_score=getattr(
                        item,
                        "identity_score",
                        0.0,
                    ),
                    document_authority_score=getattr(
                        item,
                        "document_authority_score",
                        0.0,
                    ),
                )
            )

        return results