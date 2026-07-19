"""
Retrieval service.
"""

from __future__ import annotations

from athena.domain.ai.question import Question
from athena.domain.ai.retrieval_result import RetrievalResult


class RetrievalService:
    """Retrieve relevant evidence for a question."""

    def retrieve(
        self,
        question: Question,
    ) -> list[RetrievalResult]:
        """
        Retrieve evidence supporting the supplied question.

        Parameters
        ----------
        question:
            User question.

        Returns
        -------
        list[RetrievalResult]
            Ranked retrieval results.
        """
        del question

        # TODO:
        # Integrate with DocumentSearchService.
        return []
