"""
Ask Athena page.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from athena.ai.rag.service import RAGService


class AskAthenaPage(QWidget):
    """AI question answering workspace."""

    document_requested = Signal(Path, int)

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        """Initialize Ask Athena page."""
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

        self.sources = QTreeWidget()
        self.sources.setHeaderLabels(
            [
                "Document",
                "Page",
                "Similarity",
            ]
        )
        self.sources.setRootIsDecorated(False)
        self.sources.setAlternatingRowColors(True)
        self.sources.setMaximumHeight(180)
        self.sources.itemDoubleClicked.connect(
            self._open_source,
        )

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
        """Create page layout."""

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
        """Clear question, answer and sources."""

        self.question.clear()
        self.answer.clear()
        self.sources.clear()

        if self._rag_service is None:
            self.status.setText("No workspace open")
        else:
            self.status.setText("Ready")

    def copy_answer(self) -> None:
        """Copy answer to the clipboard."""

        QApplication.clipboard().setText(
            self.answer.toPlainText(),
        )

        self.status.setText("Answer copied to clipboard")

    def ask_question(self) -> None:
        """Ask Athena a question."""

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
            self.status.setText(
                "Searching indexed documents...",
            )

            result = self._rag_service.answer(
                question,
            )

            self.answer.setPlainText(
                result.answer,
            )

            self.sources.clear()

            for source in result.sources:

                similarity = int(source.score * 100)

                item = QTreeWidgetItem(
                    [
                        source.document_name or str(source.document_id),
                        str(source.page_number),
                        f"{similarity}%",
                    ]
                )

                # Store metadata for future navigation.
                if hasattr(
                    source,
                    "document_path",
                ):
                    item.setData(
                        0,
                        Qt.ItemDataRole.UserRole,
                        str(source.document_path),
                    )

                item.setData(
                    1,
                    Qt.ItemDataRole.UserRole,
                    source.page_number,
                )

                self.sources.addTopLevelItem(
                    item,
                )

            self.status.setText(
                f"Completed ({len(result.sources)} sources)",
            )

        except Exception as exc:

            self.answer.clear()
            self.sources.clear()

            self.status.setText(
                f"Error: {exc}",
            )

        finally:

            self.ask_button.setEnabled(True)

    def _open_source(
        self,
        item: QTreeWidgetItem,
        column: int,
    ) -> None:
        """Open a cited source document."""

        del column

        path = item.data(
            0,
            Qt.ItemDataRole.UserRole,
        )

        page = item.data(
            1,
            Qt.ItemDataRole.UserRole,
        )

        if path is None:
            return

        self.document_requested.emit(
            Path(path),
            int(page),
        )
