"""
Indexed Documents page.
"""

from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QWidget

from athena.indexing.services.indexed_document_service import (
    IndexedDocumentService,
)
from athena.presentation.documents.document_browser_widget import (
    DocumentBrowserWidget,
)


class IndexedDocumentsPage(QWidget):
    """Displays indexed documents."""

    def __init__(
        self,
        service: IndexedDocumentService | None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._service = service

        layout = QVBoxLayout(self)

        self._browser = DocumentBrowserWidget(
            service=service,
        )

        layout.addWidget(
            self._browser,
        )

    def set_document_service(
        self,
        service: IndexedDocumentService,
    ) -> None:
        """Attach a document service after a workspace is opened."""

        self._service = service

        self._browser.set_document_service(
            service,
        )

        self._browser.refresh()

    @property
    def browser(
        self,
    ) -> DocumentBrowserWidget:
        """Return the embedded document browser."""

        return self._browser
