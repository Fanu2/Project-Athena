"""
AI application service.
"""

from __future__ import annotations

from athena.application.ai.prompt_builder import PromptBuilder
from athena.application.ai.retrieval_service import RetrievalService
from athena.domain.ai.answer import Answer
from athena.domain.ai.configuration import AIConfiguration
from athena.domain.ai.question import Question
from athena.infrastructure.llm.provider import LLMProvider


class AIService:
    """Coordinate the AI workflow."""

    def __init__(
        self,
        retrieval_service: RetrievalService,
        prompt_builder: PromptBuilder,
        provider: LLMProvider,
        configuration: AIConfiguration,
    ) -> None:
        self._retrieval_service = retrieval_service
        self._prompt_builder = prompt_builder
        self._provider = provider
        self._configuration = configuration

    def ask(
        self,
        question: Question,
    ) -> Answer:
        """
        Answer a user's question.

        Parameters
        ----------
        question:
            The user's question.

        Returns
        -------
        Answer
            AI-generated answer with citations.
        """

        evidence = self._retrieval_service.retrieve(
            question,
        )

        prompt = self._prompt_builder.build(
            question,
            evidence,
        )

        response = self._provider.generate(
            prompt,
            self._configuration,
        )

        return Answer(
            text=response,
            citations=[],
        )
