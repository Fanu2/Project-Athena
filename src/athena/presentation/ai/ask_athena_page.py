"""
Ask Athena page.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from athena.ai.rag.service import RAGService


class AskAthenaPage(QWidget):
    """AI question answering workspace."""

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._rag_service: RAGService | None = None

        self.question = QTextEdit()

        self.question.setPlaceholderText("Ask Athena about your documents...")

        self.ask_button = QPushButton(
            "Ask",
        )

        self.answer = QTextEdit()

        self.answer.setReadOnly(
            True,
        )

        self.status = QLabel(
            "Ready",
        )

        self._setup_ui()

        self.ask_button.clicked.connect(
            self.ask_question,
        )

    def _setup_ui(self) -> None:
        """Create layout."""

        layout = QVBoxLayout(self)

        layout.addWidget(
            self.question,
        )

        layout.addWidget(
            self.ask_button,
        )

        layout.addWidget(
            self.answer,
        )

        layout.addWidget(
            self.status,
        )

    def set_rag_service(
        self,
        service: RAGService,
    ) -> None:
        """Attach RAG service."""

        self._rag_service = service

    def clear_rag_service(self) -> None:
        """Remove RAG service."""

        self._rag_service = None

        self.answer.clear()

        self.status.setText(
            "No workspace open",
        )

    def ask_question(self) -> None:
        """Send question to Athena."""

        if self._rag_service is None:
            self.status.setText(
                "No AI service available",
            )
            return

        question = self.question.toPlainText().strip()

        if not question:
            self.status.setText(
                "Please enter a question",
            )
            return

        self.status.setText(
            "Searching documents...",
        )

        result = self._rag_service.answer(
            question,
        )

        sources = "\n".join(
            [
                (
                    f"{source.document_name or source.document_id} "
                    f"(page {source.page_number}, "
                    f"score {source.score:.2f})"
                )
                for source in result.sources
            ],
        )

        self.answer.setText(
            result.answer + "\n\nSources:\n" + sources,
        )

        self.status.setText(
            "Completed",
        )
