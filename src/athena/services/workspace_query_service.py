"""
Workspace query service.

Provides structured information about the Athena workspace.
"""

from __future__ import annotations

from athena.ai.rag.models import RAGAnswer
from athena.indexing.services.indexed_document_service import (
    IndexedDocumentService,
)


class WorkspaceQueryService:
    """Provides workspace-level information."""

    def __init__(
        self,
        indexed_document_service: IndexedDocumentService,
    ) -> None:
        self._indexed_documents = indexed_document_service

    def list_documents(self):
        """Return indexed documents."""

        return self._indexed_documents.list_documents()

    def library_summary(self) -> dict[str, int]:
        """Return workspace statistics."""

        documents = self.list_documents()

        return {
            "documents": len(documents),
            "pages": sum(document.page_count for document in documents),
        }

    def describe_library(self) -> RAGAnswer:
        """Return human-readable library description."""

        documents = self.list_documents()

        if not documents:
            return RAGAnswer(
                answer="No indexed documents.",
                model="workspace",
                sources=[],
                retrieval_results=[],
            )

        lines = [
            f"Documents: {len(documents)}",
            f"Pages: {sum(d.page_count for d in documents)}",
            "",
        ]

        for document in documents:
            lines.append(
                f"{document.title}\nPages: {document.page_count}\nIndexed: {document.indexed_at}"
            )

        return RAGAnswer(
            answer="\n\n".join(lines),
            model="workspace",
            sources=[],
            retrieval_results=[],
        )

