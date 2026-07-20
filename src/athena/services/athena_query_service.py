"""
Athena query service.

Routes questions between workspace intelligence
and document RAG.
"""

from __future__ import annotations

from athena.ai.rag.service import RAGService

from athena.services.workspace_query_service import (
    WorkspaceQueryService,
)


class AthenaQueryService:
    """Unified question service for Athena."""

    def __init__(
        self,
        rag_service: RAGService,
        workspace_service: WorkspaceQueryService,
    ) -> None:
        self._rag_service = rag_service
        self._workspace_service = workspace_service

    def answer(
        self,
        question: str,
    ):
        """Answer a user question."""

        if self._is_workspace_question(
            question,
        ):
            return self._workspace_service.describe_library()

        return self._rag_service.answer(
            question,
        )

    def _is_workspace_question(
        self,
        question: str,
    ) -> bool:
        """Detect workspace questions."""

        text = question.lower()

        keywords = [
            "documents",
            "document list",
            "indexed",
            "library",
            "how many pages",
            "how many documents",
            "my files",
        ]

        return any(
            keyword in text
            for keyword in keywords
        )