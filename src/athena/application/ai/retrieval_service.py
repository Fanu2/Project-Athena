"""
Retrieval service.
"""

from __future__ import annotations

from athena.ai.retrieval.evidence_explainer import (
    EvidenceExplainer,
)
from athena.ai.retrieval.service import (
    RetrievalService as SemanticRetrievalService,
)
from athena.domain.ai.evidence_record import (
    EvidenceRecord,
)
from athena.domain.ai.question import (
    Question,
)
from athena.domain.ai.retrieval_result import (
    RetrievalResult,
)


class RetrievalService:
    """Retrieve relevant evidence for a question."""

    def __init__(
        self,
        semantic_retrieval_service: SemanticRetrievalService,
    ) -> None:
        self._semantic_retrieval_service = (
            semantic_retrieval_service
        )

        self._evidence_explainer = EvidenceExplainer()

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

        semantic_results = (
            self._semantic_retrieval_service.search_similar(
                query=question.text,
            )
        )

        results: list[RetrievalResult] = []

        for item in semantic_results:
            results.append(
                RetrievalResult(
                    document_id=item.document_id,
                    document_name=item.document_name,
                    document_path=item.document_path,
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

    def retrieve_evidence(
        self,
        question: Question,
    ) -> list[EvidenceRecord]:
        """
        Retrieve authoritative evidence records.
        """

        semantic_results = (
            self._semantic_retrieval_service.search_similar(
                query=question.text,
            )
        )

        records: list[EvidenceRecord] = []

        for item in semantic_results:
            semantic_score = getattr(
                item,
                "semantic_score",
                item.score,
            )

            keyword_score = getattr(
                item,
                "keyword_score",
                0.0,
            )

            metadata_score = getattr(
                item,
                "metadata_score",
                0.0,
            )

            identity_score = getattr(
                item,
                "identity_score",
                0.0,
            )

            document_authority_score = getattr(
                item,
                "document_authority_score",
                0.0,
            )

            records.append(
                EvidenceRecord(
                    document_id=item.document_id,
                    document_name=item.document_name,
                    document_path=item.document_path,
                    chunk_id=item.chunk_id,
                    page=item.page_number,
                    text=item.text,
                    semantic_score=semantic_score,
                    keyword_score=keyword_score,
                    metadata_score=metadata_score,
                    identity_score=identity_score,
                    document_authority_score=document_authority_score,
                    final_score=item.score,
                    ranking_reasons=(
                        self._evidence_explainer.explain(
                            semantic_score=semantic_score,
                            keyword_score=keyword_score,
                            metadata_score=metadata_score,
                            identity_score=identity_score,
                            document_authority_score=document_authority_score,
                        )
                    ),
                )
            )

        return records