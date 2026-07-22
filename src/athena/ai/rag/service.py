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
from athena.ai.metadata.service import MetadataService


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

    def answer(
        self,
        question: str,
    ) -> RAGAnswer:
        """
        Generate an answer using retrieved document context.
        """

        #
        # Detect user intent
        #

        intent = self._intent_service.detect(question)

        metadata = self._metadata_service.detect(question)

        #
        # Retrieve relevant chunks
        #

        results = self._retrieval.search_similar(
            question,
            limit=self._retrieval_limit,
            metadata=metadata,
        )

        #
        # Build context from retrieved sources
        #

        context = self._context_builder.build(
            question,
            results,
        )

        #
        # Build final user prompt
        #

        prompt = self._prompt_builder.build(
            question=question,
            context=context.context,
            intent=intent,
        )

        #
        # Create LLM request
        #

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

        #
        # Generate response
        #

        response = self._llm.generate(
            request,
        )

        #
        # Return structured RAG answer
        #

        return RAGAnswer(
            answer=response.text,
            model=response.model,
            sources=context.sources,
            retrieval_results=results,
        )