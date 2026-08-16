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
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QSplitter,
    QPushButton,
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

from athena.presentation.ai.evidence_widget import (
    EvidenceWidget,
)

from athena.presentation.retrieval.retrieval_inspector_widget import (
RetrievalInspectorWidget,
)

from athena.presentation.ai.conversation_model import (
    ConversationModel,
)

from athena.presentation.ai.conversation_widget import (
    ConversationWidget,
)

from athena.presentation.widgets.assistant_plan import (
    AssistantPlanWidget,
)




class AskAthenaPage(QWidget):
    """AI question answering workspace."""

    document_requested = Signal(Path, int)

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        """
        Initialize Ask Athena page.
        """

        super().__init__(
            parent,
        )


        #
        # Services
        #

        self._query_service: ConversationQueryService | None = None

        self._conversation_service: ConversationService | None = None

        self._conversation_service_path: Path | None = None

        #
        # Assistant Engine (A22.6)
        #

        self._assistant_engine = None

        self._workspace_snapshot = None


        #
        # Workspace Context (A20.7)
        #

        self.workspace_label = QLabel(
            "Workspace: -",
        )

        self.workspace_stats_label = QLabel(
            "Workspace Intelligence: -",
        )


        #
        # Question input
        #

        self.question = QTextEdit()

        self.question.setPlaceholderText(
            "Ask Athena about your indexed documents..."
        )

        self.question.setMaximumHeight(
            100,
        )


        #
        # Buttons
        #

        self.ask_button = QPushButton(
            "Ask",
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
        # Evidence Intelligence
        #

        self.evidence_widget = EvidenceWidget() 

        self.retrieval_inspector = RetrievalInspectorWidget()       

        #
        # Assistant Plan (A22.7)
        #

        self.assistant_plan = (
            AssistantPlanWidget()
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

        self.sources.setMaximumHeight(
            180,
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
            "Select an evidence row to view the complete retrieved passage..."
        )

        self.passage.setMaximumHeight(
            180,
        )

        self.sources.itemSelectionChanged.connect(
            self._show_selected_passage,
        )


        #
        # Status
        #

        self.status = QLabel(
            "Ready",
        )


        #
        # Current model
        #

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
        # Keyboard shortcut
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
        """Create the page layout."""

        layout = QVBoxLayout(self)

        #
        # Workspace Context
        #

        context_layout = QHBoxLayout()

        context_layout.addWidget(
            self.workspace_label,
        )

        context_layout.addWidget(
            self.workspace_stats_label,
        )

        context_layout.addStretch()

        context_layout.addWidget(
            self.model_label,
        )

        layout.addLayout(
            context_layout,
        )

        #
        # Main Conversation + Intelligence Area
        #

        main_splitter = QSplitter(
            Qt.Orientation.Horizontal,
        )

        conversation_panel = QWidget()

        conversation_layout = QVBoxLayout(
            conversation_panel,
        )

        conversation_layout.addWidget(
            QLabel("Conversation"),
        )

        conversation_layout.addWidget(
            self.conversation,
        )

        intelligence_panel = QWidget()

        intelligence_layout = QVBoxLayout(
            intelligence_panel,
        )

        intelligence_layout.addWidget(
            QLabel("Athena Intelligence"),
        )

        intelligence_layout.addWidget(
            self.citation_widget,
        )

        intelligence_layout.addWidget(
            self.evidence_widget,
        )

        intelligence_layout.addWidget(
            self.retrieval_inspector,
        )

        intelligence_layout.addWidget(
            self.assistant_plan,
        )

        main_splitter.addWidget(
            conversation_panel,
        )

        main_splitter.addWidget(
            intelligence_panel,
        )

        main_splitter.setStretchFactor(
            0,
            3,
        )

        main_splitter.setStretchFactor(
            1,
            2,
        )

        layout.addWidget(
            main_splitter,
        )

        main_splitter.setMinimumHeight(
            300,
        )

        main_splitter.setMaximumHeight(
            450,
        )

        #
        # Question Input (always visible)
        #

        layout.addWidget(
            QLabel("Question"),
        )

        layout.addWidget(
            self.question,
        )

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
        # Retrieved Evidence
        #

        layout.addWidget(
            QLabel("Retrieved Evidence"),
        )

        layout.addWidget(
            self.sources,
        )

        layout.addWidget(
            QLabel("Retrieved Passage"),
        )

        layout.addWidget(
            self.passage,
        )

        layout.addWidget(
            self.status,
        )

    def showEvent(
        self,
        event,
    ) -> None:
        """Refresh conversation when page becomes visible."""

        super().showEvent(
            event,
        )

        if self._conversation_service is not None:
            self.conversation.refresh()

    def set_query_service(
        self,
        service: ConversationQueryService,
    ) -> None:
        """Attach Athena query service."""

        self._query_service = service

        self.status.setText(
            "Ready",
        )

        self.model_label.setText(
            "Model: -",
        )


    def set_assistant_engine(
        self,
        engine,
    ) -> None:
        """
        Attach Assistant Engine.
        """

        self._assistant_engine = engine


    def set_workspace_intelligence_snapshot(
        self,
        snapshot,
    ) -> None:
        """
        Attach workspace intelligence snapshot.
        """

        self._workspace_snapshot = snapshot


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

        self.citation_widget.clear()

        self.assistant_plan.clear()

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

        #
        # Assistant Planning (A22.6)
        #

        if (
            self._assistant_engine is not None
            and self._workspace_snapshot is not None
        ):
            decision = (
                self._assistant_engine.analyze_request(
                    question,
                    self._workspace_snapshot,
                )
            )

            plan = (
                self._assistant_engine.create_plan(
                    decision,
                )
            )

            self.assistant_plan.set_plan(
                plan,
            )
            

            self.status.setText(
                (
                    f"Athena plan: "
                    f"{plan.capability}"
                ),
            )

        try:
            self.status.setText(
                "Searching Athena knowledge...",
            )

            result = self._query_service.answer(
                question,
            )
            #
            # Refresh conversation display
            #

            if self._conversation_service is not None:
                self.conversation.refresh()

            self.sources.clear()

            self.passage.clear()

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

                self.status.setText(
                    "Completed (workspace information)",
                )

                return

            #
            # RAG response with citations
            #

            self.model_label.setText(
                f"Model: {result.model}",
            )

            self.retrieval_inspector.set_results(
            result.retrieval_results,
            )

            #
            # Evidence Intelligence
            #

            if result.evidence:

                self.evidence_widget.set_evidence(
                    result.evidence[0],
                )

            else:

                self.evidence_widget.clear()

            #
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



            for index, (source, retrieval) in enumerate(
                zip(
                    result.sources,
                    result.retrieval_results,
                    strict=False,
                )
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

                #
                # Evidence intelligence explanation.
                #

                if index < len(result.evidence):
                    evidence = result.evidence[index]

                    reasons = "\n".join(
                        evidence.ranking_reasons,
                    )

                    item.setToolTip(
                        2,
                        (
                            f"Score: {evidence.final_score:.3f}\n\n"
                            f"Why selected:\n{reasons}"
                        ),
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
                    (
                        f"Completed "
                        f"({len(result.sources)} sources, "
                        f"{len(result.citations)} citations)"
                    ),
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

    def set_workspace_snapshot(
        self,
        workspace_name: str,
        snapshot,
    ) -> None:
        """
        Display workspace intelligence context.
        """

        self.workspace_label.setText(
            f"Workspace: {workspace_name}",
        )

        self.workspace_stats_label.setText(
            (
                f"Documents: {snapshot.document_count}\n"
                f"Pages: {snapshot.page_count}\n"
                f"Knowledge Items: "
                f"Conversation Messages: "
                f"{snapshot.conversation_messages}\n"
                f"Active Document: "
                f"{snapshot.active_document or '-'}"
                f"{snapshot.conversation_messages}"
            ),
        )

    def set_workspace_context(
        self,
        name: str,
        documents: int,
        pages: int,
        knowledge_items: int,
    ) -> None:
        """
        Backward compatible workspace context update.
        """

        self.workspace_label.setText(
            f"Workspace: {name}",
        )

        self.workspace_stats_label.setText(
            (
                f"Documents: {documents}\n"
                f"Pages: {pages}\n"
                f"Knowledge Items: {knowledge_items}"
            ),
        )


    def clear_workspace_context(
        self,
    ) -> None:
        """
        Clear workspace intelligence context.
        """

        if hasattr(
            self,
            "workspace_label",
        ):
            self.workspace_label.setText(
                "Workspace: -"
            )

        if hasattr(
            self,
            "workspace_stats_label",
        ):
            self.workspace_stats_label.setText(
                ""
            )

    def set_conversation_service(
        self,
        service: ConversationService,
    ) -> None:
        """Attach conversation service and restore history."""

        self._conversation_service = service

        #
        # Create conversation model
        #

        model = ConversationModel(
            service,
        )

        #
        # Attach model to widget
        #

        self.conversation.set_model(
            model,
        )

        #
        # Restore persisted conversation
        #

        self.conversation.refresh()

    def set_conversation_path(
        self,
        path: Path,
    ) -> None:
        """
        Set persistent conversation storage path.
        """

        self._conversation_service_path = path

