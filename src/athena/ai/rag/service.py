"""
RAG orchestration service.
"""

from __future__ import annotations

from athena.ai.llm.models import (
    LLMRequest,
)
from athena.ai.llm.provider import (
    LLMProvider,
)
from athena.ai.rag.context_builder import (
    ContextBuilder,
)
from athena.ai.rag.models import (
    RAGAnswer,
)
from athena.ai.rag.prompt_builder import (
    PromptBuilder,
)
from athena.ai.retrieval.service import (
    RetrievalService,
)


class RAGService:
    """Coordinate retrieval and generation."""

    def __init__(
        self,
        retrieval_service: RetrievalService,
        context_builder: ContextBuilder,
        llm_provider: LLMProvider,
        model_name: str,
        retrieval_limit: int = 5,
    ) -> None:
        """Initialize RAG service."""

        self._retrieval = retrieval_service

        self._context_builder = context_builder

        self._llm = llm_provider

        self._model_name = model_name

        self._retrieval_limit = retrieval_limit

        self._prompt_builder = PromptBuilder()

    def answer(
        self,
        question: str,
    ) -> RAGAnswer:
        """Generate an answer using retrieved context."""

        results = self._retrieval.search_similar(
            question,
            limit=self._retrieval_limit,
        )

        context = self._context_builder.build(
            question,
            results,
        )

        prompt = self._prompt_builder.build(
            question,
            context.context,
        )

        request = LLMRequest(
            prompt=prompt,
            model_name=self._model_name,
        )

        response = self._llm.generate(
            request,
        )

        return RAGAnswer(
            answer=response.text,
            sources=context.sources,
        )
