from pathlib import Path

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
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from athena.application.conversation.conversation_query_service import (
    ConversationQueryService,
)

from athena.conversation.service import (
    ConversationService,
)

from athena.presentation.ai.citation_widget import (
    CitationWidget,
)

from athena.presentation.ai.conversation_model import (
    ConversationModel,
)

from athena.presentation.ai.conversation_widget import (
    ConversationWidget,
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

        self._query_service: (
            ConversationQueryService | None
        ) = None

        self._conversation_service: (
            ConversationService | None
        ) = None

        #
        # Workspace Intelligence Context
        #

        self.workspace_context = QLabel(
            "No workspace open",
        )

        self.workspace_context.setWordWrap(
            True,
        )

        #
        # Question Input
        #

        self.question = QTextEdit()

        self.question.setPlaceholderText(
            "Ask Athena about your workspace documents..."
        )

        self.question.setMaximumHeight(
            120,
        )

        #
        # Action Buttons
        #

        self.ask_button = QPushButton(
            "Ask Athena",
        )

        self.clear_button = QPushButton(
            "Clear",
        )

        self.copy_button = QPushButton(
            "Copy Answer",
        )

        #
        # Conversation
        #

        self.conversation = ConversationWidget()

        #
        # Citation Intelligence
        #

        self.citation_widget = CitationWidget()

        self.citation_widget.document_requested.connect(
            self.document_requested.emit,
        )

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

        self.sources.setRootIsDecorated(
            False,
        )

        self.sources.setAlternatingRowColors(
            True,
        )

        self.sources.itemDoubleClicked.connect(
            self._open_source,
        )

        #
        # Retrieved Passage
        #

        self.passage = QPlainTextEdit()

        self.passage.setReadOnly(
            True,
        )

        self.passage.setPlaceholderText(
            "Select evidence to view the complete retrieved passage..."
        )

        self.sources.itemSelectionChanged.connect(
            self._show_selected_passage,
        )

        #
        # Runtime Status
        #

        self.status = QLabel(
            "Ready",
        )

        self.model_label = QLabel(
            "Model: -",
        )

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

        #
        # Ctrl + Enter shortcut
        #

        shortcut = QShortcut(
            QKeySequence(
                Qt.KeyboardModifier.ControlModifier
                | Qt.Key.Key_Return,
            ),
            self,
        )

        shortcut.activated.connect(
            self.ask_question,
        )
    def _setup_ui(self) -> None:
        """Create Ask Athena research dashboard."""

        layout = QVBoxLayout(
            self,
        )

        layout.setContentsMargins(
            12,
            12,
            12,
            12,
        )

        layout.setSpacing(
            10,
        )

        #
        # Workspace Context
        #

        context_box = QGroupBox(
            "Workspace Context",
        )

        context_layout = QVBoxLayout(
            context_box,
        )

        self.workspace_context.setStyleSheet(
            """
            QLabel {
                font-size: 13px;
                padding: 6px;
            }
            """
        )

        context_layout.addWidget(
            self.workspace_context,
        )

        layout.addWidget(
            context_box,
        )


        #
        # Question Panel
        #

        question_box = QGroupBox(
            "Ask Athena",
        )

        question_layout = QVBoxLayout(
            question_box,
        )

        self.question.setMinimumHeight(
            80,
        )

        question_layout.addWidget(
            self.question,
        )


        button_layout = QHBoxLayout()

        self.ask_button.setMinimumWidth(
            120,
        )

        self.copy_button.setMinimumWidth(
            120,
        )

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


        question_layout.addLayout(
            button_layout,
        )

        layout.addWidget(
            question_box,
        )


        #
        # Athena Runtime Status
        #

        status_box = QGroupBox(
            "Athena Status",
        )

        status_layout = QHBoxLayout(
            status_box,
        )

        status_layout.addWidget(
            self.status,
        )

        status_layout.addStretch()

        status_layout.addWidget(
            self.model_label,
        )

        layout.addWidget(
            status_box,
        )


        #
        # Conversation Panel
        #

        conversation_box = QGroupBox(
            "Conversation",
        )

        conversation_layout = QVBoxLayout(
            conversation_box,
        )

        conversation_layout.addWidget(
            self.conversation,
        )


        #
        # Evidence Panel
        #

        evidence_box = QGroupBox(
            "Retrieved Evidence",
        )

        evidence_layout = QVBoxLayout(
            evidence_box,
        )

        self.sources.setColumnWidth(
            0,
            230,
        )

        self.sources.setColumnWidth(
            1,
            60,
        )

        self.sources.setColumnWidth(
            2,
            90,
        )

        evidence_layout.addWidget(
            self.sources,
        )


        #
        # Citation Intelligence Panel
        #

        citation_box = QGroupBox(
            "Citation Intelligence",
        )

        citation_layout = QVBoxLayout(
            citation_box,
        )

        citation_layout.addWidget(
            self.citation_widget,
        )


        #
        # Evidence + Citation Split
        #

        evidence_splitter = QSplitter(
            Qt.Orientation.Horizontal,
        )

        evidence_splitter.addWidget(
            evidence_box,
        )

        evidence_splitter.addWidget(
            citation_box,
        )

        evidence_splitter.setStretchFactor(
            0,
            3,
        )

        evidence_splitter.setStretchFactor(
            1,
            2,
        )


        #
        # Conversation + Evidence Split
        #

        main_splitter = QSplitter(
            Qt.Orientation.Vertical,
        )

        main_splitter.addWidget(
            conversation_box,
        )

        main_splitter.addWidget(
            evidence_splitter,
        )

        main_splitter.setStretchFactor(
            0,
            5,
        )

        main_splitter.setStretchFactor(
            1,
            3,
        )


        layout.addWidget(
            main_splitter,
            1,
        )


        #
        # Retrieved Passage
        #

        passage_box = QGroupBox(
            "Retrieved Passage",
        )

        passage_layout = QVBoxLayout(
            passage_box,
        )

        passage_layout.addWidget(
            self.passage,
        )

        layout.addWidget(
            passage_box,
        )


        #
        # Athena visual theme
        #

        self.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold;
                border: 1px solid palette(mid);
                border-radius: 8px;
                margin-top: 8px;
                padding-top: 8px;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }

            QPushButton {
                padding: 6px 14px;
                border-radius: 5px;
            }

            QTextEdit,
            QPlainTextEdit,
            QTreeWidget {
                border-radius: 5px;
            }
            """
        )
        #
        # Workspace Intelligence Context
        #

    def set_workspace_context(
        self,
        name: str,
        documents: int,
        pages: int,
        knowledge_items: int,
    ) -> None:
        """
        Display workspace intelligence summary.
        """

        self.workspace_context.setText(
            (
                f"<b>Workspace:</b> {name}<br>"
                f"Documents: {documents} | "
                f"Pages: {pages} | "
                f"Knowledge Items: {knowledge_items}"
            )
        )


    def clear_workspace_context(
        self,
    ) -> None:
        """
        Clear workspace summary.
        """

        self.workspace_context.setText(
            "No workspace open",
        )


    #
    # Status handling
    #

    def set_status(
        self,
        message: str,
    ) -> None:
        """
        Update Athena status.
        """

        self.status.setText(
            message,
        )


    #
    # Research view reset
    #

    def reset_research_view(
        self,
    ) -> None:
        """
        Reset evidence and citation panels.
        """

        self.sources.clear()

        self.citation_widget.clear()

        self.passage.clear()

        self.set_status(
            "Ready",
        )
    def ask_question(
        self,
    ) -> None:
        """Ask Athena a question."""

        if self._query_service is None:
            self.set_status(
                "No AI service available",
            )
            return

        question = (
            self.question
            .toPlainText()
            .strip()
        )

        if not question:
            self.set_status(
                "Please enter a question",
            )
            return

        self.ask_button.setEnabled(
            False,
        )

        try:
            self.set_status(
                "Searching workspace knowledge...",
            )

            result = (
                self._query_service
                .answer(question)
            )

            if self._conversation_service is not None:
                self.conversation.refresh()


            #
            # Clear previous research results
            #

            self.sources.clear()

            self.passage.clear()

            self.citation_widget.clear()


            #
            # Workspace intelligence response
            #

            if isinstance(
                result,
                str,
            ):
                self.model_label.setText(
                    "Model: Built-in",
                )

                self.set_status(
                    "Completed • workspace information",
                )

                return


            #
            # RAG response
            #

            self.model_label.setText(
                f"Model: {result.model}",
            )


            #
            # Citation Intelligence
            #

            if result.resolved_citations:

                self.citation_widget.set_citations(
                    result.resolved_citations,
                    result.citation_validations,
                )

            else:

                self.citation_widget.clear()


            #
            # Evidence Intelligence
            #

            for index, (
                source,
                retrieval,
            ) in enumerate(
                zip(
                    result.sources,
                    result.retrieval_results,
                    strict=False,
                )
            ):

                similarity = int(
                    source.score * 100,
                )

                preview = (
                    retrieval.text
                    .replace(
                        "\n",
                        " ",
                    )
                    .strip()
                )

                if len(preview) > 100:
                    preview = (
                        preview[:100]
                        + "..."
                    )


                item = QTreeWidgetItem(
                    [
                        (
                            source.document_name
                            or str(source.document_id)
                        ),
                        str(
                            source.page_number,
                        ),
                        f"{similarity}%",
                        preview,
                    ]
                )


                #
                # Evidence explanation
                #

                if index < len(
                    result.evidence,
                ):

                    evidence = (
                        result.evidence[index]
                    )

                    reasons = "\n".join(
                        evidence.ranking_reasons,
                    )

                    item.setToolTip(
                        2,
                        (
                            f"Score: "
                            f"{evidence.final_score:.3f}"
                            "\n\n"
                            "Why selected:\n"
                            f"{reasons}"
                        ),
                    )


                #
                # Store passage
                #

                item.setData(
                    3,
                    Qt.ItemDataRole.UserRole,
                    retrieval.text,
                )


                #
                # Source navigation
                #

                if hasattr(
                    source,
                    "document_path",
                ):

                    item.setData(
                        0,
                        Qt.ItemDataRole.UserRole,
                        str(
                            source.document_path,
                        ),
                    )


                item.setData(
                    1,
                    Qt.ItemDataRole.UserRole,
                    source.page_number,
                )


                item.setToolTip(
                    0,
                    "Double click to open source document",
                )


                self.sources.addTopLevelItem(
                    item,
                )


            self.set_status(
                (
                    f"Completed • "
                    f"{len(result.sources)} sources • "
                    f"{len(result.citations)} citations"
                ),
            )


        except Exception as exc:

            self.sources.clear()

            self.passage.clear()

            self.citation_widget.clear()


            if self._conversation_service is not None:

                self._conversation_service.add_system_message(
                    f"Error: {exc}",
                )

                self.conversation.refresh()


            self.model_label.setText(
                "Model: -",
            )

            self.set_status(
                f"Error: {exc}",
            )


        finally:

            self.ask_button.setEnabled(
                True,
            )

