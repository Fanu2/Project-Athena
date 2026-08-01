"""
RAG orchestration service.
"""

from __future__ import annotations

from athena.ai.intent.service import IntentService
from athena.ai.llm.models import (
    LLMRequest,
)
from athena.ai.llm.provider import (
    LLMProvider,
)
from athena.ai.metadata.service import MetadataService
from athena.ai.rag.context_builder import (
    ContextBuilder,
)
from athena.ai.rag.models import (
    RAGAnswer,
)
from athena.ai.rag.prompt_builder import (
    PromptBuilder,
)
from athena.application.ai.citation_service import (
    CitationService,
)
from athena.application.ai.citation_explanation_service import (
    CitationExplanationService,
)
from athena.application.ai.retrieval_service import (
    RetrievalService,
)
from athena.domain.ai.question import (
    Question,
)


class RAGService:
    """Coordinate retrieval, intent detection, and response generation."""

    def __init__(
        self,
        retrieval_service: RetrievalService,
        context_builder: ContextBuilder,
        llm_provider: LLMProvider,
        intent_service: IntentService,
        metadata_service: MetadataService,
        model_name: str,
        retrieval_limit: int = 5,
    ) -> None:
        """Initialize the RAG service."""

        self._retrieval = retrieval_service

        self._context_builder = context_builder

        self._llm = llm_provider

        self._intent_service = intent_service

        self._metadata_service = metadata_service

        self._model_name = model_name

        self._retrieval_limit = retrieval_limit

        self._prompt_builder = PromptBuilder()

        self._citation_service = CitationService()

        self._citation_explanation_service = (
            CitationExplanationService()
        )

    def answer(
        self,
        question: str,
    ) -> RAGAnswer:
        """
        Generate an answer using retrieved document context.
        """

        intent = self._intent_service.detect(
            question,
        )

        self._metadata_service.detect(
            question,
        )

        question_object = Question(
            text=question,
        )

        results = self._retrieval.retrieve(
            question_object,
        )

        evidence = self._retrieval.retrieve_evidence(
            question_object,
        )

        citations = self._citation_service.create_citations(
            evidence,
        )

        resolved_citations = (
            self._citation_explanation_service.resolve(
                citations,
                evidence,
            )
        )

        context = self._context_builder.build(
            question,
            results,
        )

        prompt = self._prompt_builder.build(
            question=question,
            context=context.context,
            intent=intent,
        )

        request = LLMRequest(
            system_prompt=(
                "You are Athena, an offline AI research assistant. "
                "Answer the user's question using only the provided "
                "document context. If the answer is not present in "
                "the context, say that the information is not available."
            ),
            user_prompt=prompt,
            model_name=self._model_name,
        )

        response = self._llm.analyze(
            request,
        )

        return RAGAnswer(
            answer=response.text,
            model=response.model,
            sources=context.sources,
            retrieval_results=results,
            evidence=evidence,
            citations=citations,
            resolved_citations=resolved_citations,
        )