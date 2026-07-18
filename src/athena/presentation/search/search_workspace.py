"""
Search workspace widget.
"""

from __future__ import annotations

from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from athena.documents.service import DocumentService
from athena.presentation.search.search_result_viewer import (
    SearchResultViewer,
)
from athena.presentation.search.search_results_model import (
    SearchResultsModel,
)
from athena.search.search_service import SearchService


class SearchWorkspace(QWidget):
    """Search interface."""

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._search_service: SearchService | None = None

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search documents...",
        )

        self.search_button = QPushButton(
            "Search",
        )

        self.results_view = QListView()

        self.status_label = QLabel(
            "Ready",
        )

        self.results_model = SearchResultsModel()

        self.results_view.setModel(
            self.results_model,
        )

        self.viewer = SearchResultViewer()

        self._setup_ui()

        self.search_button.clicked.connect(
            self.perform_search,
        )

        self.search_input.returnPressed.connect(
            self.perform_search,
        )

        self.results_view.clicked.connect(
            self._on_result_selected,
        )

    def _setup_ui(self) -> None:
        """Create widget layout."""

        main_layout = QVBoxLayout(self)

        search_layout = QHBoxLayout()

        search_layout.addWidget(
            self.search_input,
        )

        search_layout.addWidget(
            self.search_button,
        )

        main_layout.addLayout(
            search_layout,
        )

        splitter = QSplitter()

        splitter.addWidget(
            self.results_view,
        )

        splitter.addWidget(
            self.viewer,
        )

        main_layout.addWidget(
            splitter,
        )

        main_layout.addWidget(
            self.status_label,
        )

    def set_search_service(
        self,
        service: SearchService,
    ) -> None:
        """Attach search service."""

        self._search_service = service

    def set_document_service(
        self,
        service: DocumentService,
    ) -> None:
        """Attach document service."""

        self.viewer.set_document_service(
            service,
        )

    def clear_search_service(self) -> None:
        """Remove search service."""

        self._search_service = None

        self.results_model.set_results([])

        self.viewer.clear()

        self.status_label.setText(
            "No workspace open",
        )

    def perform_search(self) -> None:
        """Execute search."""

        if self._search_service is None:
            self.status_label.setText(
                "No workspace open",
            )
            return

        query = self.search_input.text()

        results = self._search_service.search(
            query,
        )

        self.results_model.set_results(
            results,
        )

        self.viewer.clear()

        self.status_label.setText(
            f"{len(results)} result(s)",
        )

    def _on_result_selected(
        self,
        index: QModelIndex,
    ) -> None:
        """Display selected result."""

        chunk = self.results_model.get_chunk(
            index.row(),
        )

        if chunk is None:
            self.viewer.clear()
            return

        self.viewer.show_chunk(
            chunk,
        )
