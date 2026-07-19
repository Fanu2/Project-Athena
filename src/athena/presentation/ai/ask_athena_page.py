"""
Ask Athena page.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
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
        self.question.setPlaceholderText("Ask Athena about your indexed documents...")
        self.question.setMaximumHeight(100)

        self.ask_button = QPushButton("Ask")

        self.clear_button = QPushButton("Clear")

        self.copy_button = QPushButton("Copy Answer")

        self.answer = QTextEdit()
        self.answer.setReadOnly(True)

        self.sources = QTextEdit()
        self.sources.setReadOnly(True)
        self.sources.setMaximumHeight(140)

        self.status = QLabel("Ready")

        self._setup_ui()

        self.ask_button.clicked.connect(
            self.ask_question,
        )

        self.clear_button.clicked.connect(
            self.clear_page,
        )

        self.copy_button.clicked.connect(
            self.copy_answer,
        )

        shortcut = QShortcut(
            QKeySequence(
                Qt.KeyboardModifier.ControlModifier | Qt.Key.Key_Return,
            ),
            self,
        )

        shortcut.activated.connect(
            self.ask_question,
        )

    def _setup_ui(self) -> None:
        """Create layout."""

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Question"))
        layout.addWidget(self.question)

        button_layout = QHBoxLayout()

        button_layout.addWidget(self.ask_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.copy_button)

        button_layout.addStretch()

        layout.addLayout(button_layout)

        layout.addWidget(self.status)

        layout.addWidget(QLabel("Answer"))
        layout.addWidget(self.answer)

        layout.addWidget(QLabel("Sources"))
        layout.addWidget(self.sources)

    def set_rag_service(
        self,
        service: RAGService,
    ) -> None:
        """Attach RAG service."""

        self._rag_service = service

        self.status.setText("Ready")

    def clear_rag_service(self) -> None:
        """Detach RAG service."""

        self._rag_service = None

        self.clear_page()

        self.status.setText("No workspace open")

    def clear_page(self) -> None:
        """Clear the workspace."""

        self.question.clear()

        self.answer.clear()

        self.sources.clear()

        if self._rag_service is None:
            self.status.setText("No workspace open")
        else:
            self.status.setText("Ready")

    def copy_answer(self) -> None:
        """Copy answer to clipboard."""

        QApplication.clipboard().setText(
            self.answer.toPlainText(),
        )

        self.status.setText("Answer copied to clipboard")

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

        self.ask_button.setEnabled(False)

        try:
            self.status.setText("Searching indexed documents...")

            result = self._rag_service.answer(
                question,
            )

            self.answer.setPlainText(
                result.answer,
            )

            source_lines = []

            for source in result.sources:

                similarity = int(source.score * 100)

                source_lines.append(
                    (
                        f"{source.document_name or source.document_id}\n"
                        f"Page: {source.page_number}\n"
                        f"Similarity: {similarity}%"
                    )
                )

            self.sources.setPlainText("\n\n".join(source_lines))

            self.status.setText(f"Completed ({len(result.sources)} sources)")

        except Exception as exc:

            self.answer.clear()

            self.sources.clear()

            self.status.setText(f"Error: {exc}")

        finally:

            self.ask_button.setEnabled(True)
