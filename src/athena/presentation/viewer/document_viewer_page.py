"""
Document viewer page.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from athena.application.viewer import DocumentViewerService

from .pdf_canvas import PDFCanvas


class DocumentViewerPage(QWidget):
    """
    Document viewing page.

    Coordinates the viewer service with the
    presentation widgets.
    """

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        """Initialize the document viewer page."""

        super().__init__(parent)

        self._service: DocumentViewerService | None = None

        self.canvas = PDFCanvas()

        self.previous_button = QPushButton(
            "◀ Previous",
        )

        self.next_button = QPushButton(
            "Next ▶",
        )

        self.page_label = QLabel(
            "Page 0 / 0",
        )

        self.status_label = QLabel(
            "No document loaded",
        )

        self._build_ui()

        self.previous_button.clicked.connect(
            self.previous_page,
        )

        self.next_button.clicked.connect(
            self.next_page,
        )

    def _build_ui(self) -> None:
        """Create the page layout."""

        layout = QVBoxLayout(
            self,
        )

        toolbar = QHBoxLayout()

        toolbar.addWidget(
            self.previous_button,
        )

        toolbar.addWidget(
            self.page_label,
        )

        toolbar.addStretch()

        toolbar.addWidget(
            self.next_button,
        )

        layout.addLayout(
            toolbar,
        )

        layout.addWidget(
            self.canvas,
            stretch=1,
        )

        layout.addWidget(
            self.status_label,
        )

    def set_viewer_service(
        self,
        service: DocumentViewerService,
    ) -> None:
        """Attach viewer service."""

        self._service = service

        self._refresh()

    def clear_viewer_service(
        self,
    ) -> None:
        """Detach viewer service."""

        self._service = None

        self.canvas.clear()

        self.page_label.setText(
            "Page 0 / 0",
        )

        self.status_label.setText(
            "No document loaded",
        )

    def open_document(
        self,
        path: Path,
        page: int | None = None,
    ) -> None:
        """
        Open a document.

        Only supported viewer formats should
        reach this page.
        """

        if self._service is None:
            return

        if not path.exists():
            self.status_label.setText(
                f"File not found: {path}",
            )
            return

        self._service.open_document(
            path,
        )

        if page is not None:
            self._go_to_page(
                page,
            )

        self._refresh()

    def _go_to_page(
        self,
        page: int,
    ) -> None:
        """Navigate safely to a page."""

        if self._service is None:
            return

        if self._service.page_count <= 0:
            return

        #
        # Citation pages may be stale.
        # Clamp to valid range.
        #

        page = max(
            1,
            min(
                page,
                self._service.page_count,
            ),
        )

        self._service.go_to_page(
            page,
        )

    def _refresh(
        self,
    ) -> None:
        """Refresh page display."""

        if (
            self._service is None
            or not self._service.is_open
        ):
            self.canvas.clear()

            self.page_label.setText(
                "Page 0 / 0",
            )

            self.status_label.setText(
                "No document loaded",
            )

            return

        image = self._service.render_current_page()

        self.canvas.set_image(
            image,
        )

        self.page_label.setText(
            (
                f"Page "
                f"{self._service.current_page + 1}"
                f" / "
                f"{self._service.page_count}"
            ),
        )

        self.status_label.setText(
            "Ready",
        )

    def next_page(
        self,
    ) -> None:
        """Move to next page."""

        if self._service is None:
            return

        if self._service.next_page():
            self._refresh()

    def previous_page(
        self,
    ) -> None:
        """Move to previous page."""

        if self._service is None:
            return

        if self._service.previous_page():
            self._refresh()