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
        """
        Answer a user question.

        Workspace questions are handled separately.
        Document-related questions always go through RAG.
        """

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
        """
        Detect workspace information questions.

        Avoid matching generic document questions such as:
        - summarize documents
        - explain documents
        - compare documents

        Those belong to RAG.
        """

        text = question.lower().strip()

        workspace_patterns = [
            "document list",
            "list documents",
            "show documents",
            "show my documents",
            "indexed documents",
            "document library",
            "my files",
            "how many documents",
            "how many pages",
            "what is indexed",
            "what have i indexed",
        ]

        return any(
            pattern in text
            for pattern in workspace_patterns
        )