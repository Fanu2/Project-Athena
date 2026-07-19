"""
Documents page.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)

from athena.services.workspace_document_service import (
    WorkspaceDocumentService,
)

from athena.presentation.documents.documents_table import (
    DocumentsTable,
)

from athena.presentation.documents.documents_toolbar import (
    DocumentsToolbar,
)


class DocumentsPage(QWidget):
    """Workspace documents page."""

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        """Initialize the page."""

        super().__init__(parent)

        self._document_service: WorkspaceDocumentService | None = None

        self.toolbar = DocumentsToolbar()

        self.table = DocumentsTable()

        self.status_label = QLabel(
            "0 documents",
        )

        layout = QVBoxLayout(self)

        layout.addWidget(
            self.toolbar,
        )

        layout.addWidget(
            self.table,
        )

        layout.addWidget(
            self.status_label,
        )

        self.toolbar.refresh_requested.connect(
            self.refresh,
        )

    def set_document_service(
        self,
        service: WorkspaceDocumentService,
    ) -> None:
        """Assign the workspace document service."""

        self._document_service = service

        self.refresh()

    def clear_document_service(
        self,
    ) -> None:
        """Clear the current workspace."""

        self._document_service = None

        self.table.table_model.set_documents([])

        self.status_label.setText(
            "0 documents",
        )

    def refresh(
        self,
    ) -> None:
        """Reload the document list."""

        if self._document_service is None:
            self.clear_document_service()
            return

        documents = self._document_service.list_documents()

        self.table.table_model.set_documents(
            documents,
        )

        count = len(documents)

        self.status_label.setText(
            f"{count} document{'s' if count != 1 else ''}",
        )

    def set_status(
        self,
        text: str,
    ) -> None:
        """Update the status label."""

        self.status_label.setText(
            text,
        )
