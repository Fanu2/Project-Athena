from pathlib import (
    Path,
)

from PySide6.QtCore import (
    Qt,
    Signal,
)
from PySide6.QtGui import (
    QKeySequence,
    QShortcut,
)
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from athena.conversation.service import (
    ConversationService,
)
from athena.presentation.ai.conversation_model import (
    ConversationModel,
)
from athena.presentation.ai.conversation_widget import (
    ConversationWidget,
)
from athena.services.athena_query_service import (
    AthenaQueryService,
)


class AskAthenaPage(QWidget):
    """AI question answering workspace."""

    document_requested = Signal(Path, int)

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        """Initialize Ask Athena page."""
        super().__init__(parent)

        #
        # Services
        #

        self._query_service: AthenaQueryService | None = None
        self._conversation_service: ConversationService | None = None

        #
        # Question input
        #

        self.question = QTextEdit()
        self.question.setPlaceholderText("Ask Athena about your indexed documents...")
        self.question.setMaximumHeight(100)

        #
        # Buttons
        #

        self.ask_button = QPushButton("Ask")
        self.clear_button = QPushButton("Clear")
        self.copy_button = QPushButton("Copy Answer")

        #
        # Conversation
        #

        self.conversation = ConversationWidget()

        #
        # Sources
        #

        #
        # Retrieved Evidence
        #

        self.sources = QTreeWidget()

        self.sources.setHeaderLabels(
            [
                "Document",
                "Page",
                "Similarity",
                "Preview",
            ]
        )

        self.sources.setRootIsDecorated(False)

        self.sources.setAlternatingRowColors(True)

        self.sources.setMaximumHeight(180)

        self.sources.itemDoubleClicked.connect(
            self._open_source,
        )

        #
        # Retrieved Passage
        #

        self.passage = QPlainTextEdit()

        self.passage.setReadOnly(True)

        self.passage.setPlaceholderText(
            "Select an evidence row to view the complete retrieved passage..."
        )

        self.passage.setMaximumHeight(180)

        self.sources.itemSelectionChanged.connect(
            self._show_selected_passage,
        )

        #
        # Status
        #

        self.status = QLabel("Ready")

        #
        # Current model
        #

        self.model_label = QLabel("Model: -")

        #
        # Build UI
        #

        self._setup_ui()

        #
        # Signals
        #

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
        """Create the page layout."""

        layout = QVBoxLayout(self)

        #
        # Question
        #

        layout.addWidget(
            QLabel("Question"),
        )

        layout.addWidget(
            self.question,
        )

        #
        # Buttons
        #

        button_layout = QHBoxLayout()

        button_layout.addWidget(
            self.ask_button,
        )

        button_layout.addWidget(
            self.clear_button,
        )

        button_layout.addWidget(
            self.copy_button,
        )

        button_layout.addStretch()

        layout.addLayout(
            button_layout,
        )

        #
        # Status
        #

        layout.addWidget(
            self.status,
        )

        layout.addWidget(
            self.model_label,
        )

        #
        # Conversation
        #

        layout.addWidget(
            QLabel("Conversation"),
        )

        layout.addWidget(
            self.conversation,
        )

        #
        # Retrieved Evidence
        #

        layout.addWidget(
            QLabel("Retrieved Evidence"),
        )

        layout.addWidget(
            self.sources,
        )

        #
        # Retrieved Passage
        #

        layout.addWidget(
            QLabel("Retrieved Passage"),
        )

        layout.addWidget(
            self.passage,
        )
    def set_query_service(
        self,
        service: AthenaQueryService,
    ) -> None:
        """Attach Athena query service."""

        self._query_service = service

        self.status.setText(
            "Ready",
        )

        self.model_label.setText(
            "Model: -",
        )

    def clear_query_service(self) -> None:
        """Detach Athena query service."""

        self._query_service = None

        self.clear_page()

        self.status.setText(
            "No workspace open",
        )

        self.model_label.setText(
            "Model: -",
        )

    def clear_page(
        self,
    ) -> None:
        """Clear the current conversation."""

        self.question.clear()

        self.sources.clear()

        if self._conversation_service is not None:
            self._conversation_service.clear()

        self.conversation.refresh()

        self.model_label.setText(
            "Model: -",
        )

        if self._query_service is None:
            self.status.setText(
                "No workspace open",
            )
        else:
            self.status.setText(
                "Ready",
            )

    def copy_answer(
        self,
    ) -> None:
        """Copy the most recent response."""

        model = self.conversation.model()

        if model is None:
            return

        message = model.last_message()

        if message is None:
            return

        QApplication.clipboard().setText(
            message.text,
        )

        self.status.setText(
            "Latest response copied",
        )

    def ask_question(
        self,
    ) -> None:
        """Ask Athena a question."""

        if self._query_service is None:
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
                "Searching Athena knowledge...",
            )

            if self._conversation_service is not None:
                self._conversation_service.add_user_message(
                    question,
                )

                self.conversation.refresh()

            result = self._query_service.answer(
                question,
            )

            self.sources.clear()

            self.passage.clear()

            #
            # Workspace intelligence response
            #

            if isinstance(
                result,
                str,
            ):
                if self._conversation_service is not None:
                    self._conversation_service.add_assistant_message(
                        result,
                    )

                    self.conversation.refresh()

                self.model_label.setText(
                    "Model: Built-in",
                )

                self.status.setText(
                    "Completed (workspace information)",
                )

                return

            #
            # RAG response with citations
            #

            if self._conversation_service is not None:
                self._conversation_service.add_assistant_message(
                    result.answer,
                )

                self.conversation.refresh()

            self.model_label.setText(
                f"Model: {result.model}",
            )

            for source, retrieval in zip(
                result.sources,
                result.retrieval_results,
                strict=False,
            ):
                similarity = int(
                    source.score * 100,
                )

                preview = retrieval.text.replace(
                    "\n",
                    " ",
                ).strip()

                if len(preview) > 80:
                    preview = preview[:80] + "..."

                item = QTreeWidgetItem(
                    [
                        source.document_name or str(source.document_id),
                        str(source.page_number),
                        f"{similarity}%",
                        preview,
                    ]
                )

                item.setToolTip(
                    3,
                    retrieval.text,
                )

                item.setData(
                    3,
                    Qt.ItemDataRole.UserRole,
                    retrieval.text,
                )

                #
                # Store metadata for navigation.
                #

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
            self.sources.clear()

            self.passage.clear()

            if self._conversation_service is not None:
                self._conversation_service.add_system_message(
                    f"Error: {exc}",
                )

                self.conversation.refresh()

            self.model_label.setText(
                "Model: -",
            )

            self.status.setText(
                f"Error: {exc}",
            )

        finally:
            self.ask_button.setEnabled(
                True,
            )

    def _show_selected_passage(
        self,
    ) -> None:
        """Display the selected retrieved passage."""

        items = self.sources.selectedItems()

        if not items:
            self.passage.clear()
            return

        passage = items[0].data(
            3,
            Qt.ItemDataRole.UserRole,
        )

        self.passage.setPlainText(
            passage or "",
        )

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

    def set_conversation_service(
        self,
        service: ConversationService,
    ) -> None:
        """Attach conversation service."""

        self._conversation_service = service

        model = ConversationModel(
            service,
        )

        self.conversation.set_model(
            model,
        )
