"""
Assistant retrieval integration adapter.
"""

from __future__ import annotations

from athena.application.ai.retrieval_service import (
    RetrievalService,
)

from athena.domain.ai.question import (
    Question,
)


class AssistantRetrievalAdapter:
    """
    Bridges Assistant with Athena retrieval.
    """

    def __init__(
        self,
        retrieval_service: RetrievalService,
    ) -> None:

        self._retrieval = retrieval_service


    def retrieve(
        self,
        query: str,
    ):
        """
        Retrieve workspace information.
        """

        question = Question(
            text=query,
        )

        return (
            self._retrieval.retrieve(
                question,
            )
        )


    def retrieve_evidence(
        self,
        query: str,
    ):
        """
        Retrieve evidence records.
        """

        question = Question(
            text=query,
        )

        return (
            self._retrieval.retrieve_evidence(
                question,
            )
        )
