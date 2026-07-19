"""
Document viewer application service.

Coordinates document viewing between the presentation layer and the
low-level PdfRenderer.
"""

from __future__ import annotations

from PySide6.QtGui import QImage

from athena.documents.models import Document
from athena.infrastructure.viewer import PdfRenderer


class DocumentViewerService:
    """
    High-level document viewing service.

    Maintains navigation state while delegating rendering to PdfRenderer.
    """

    def __init__(
        self,
        renderer: PdfRenderer | None = None,
    ) -> None:
        """Initialize the service."""

        self._renderer = renderer or PdfRenderer()

        self._document: Document | None = None

        self._current_page = 0

    @property
    def document(self) -> Document | None:
        """Return the currently opened document."""

        return self._document

    @property
    def current_page(self) -> int:
        """Return the current zero-based page index."""

        return self._current_page

    @property
    def page_count(self) -> int:
        """Return the total number of pages."""

        return self._renderer.page_count

    @property
    def is_open(self) -> bool:
        """Return True if a document is open."""

        return self._renderer.is_open

    def open_document(
        self,
        document: Document,
    ) -> None:
        """
        Open a document.

        Args:
            document:
                Athena document model.
        """

        self._renderer.open(document.path)

        self._document = document

        self._current_page = 0

    def close(self) -> None:
        """Close the current document."""

        self._renderer.close()

        self._document = None

        self._current_page = 0

    def metadata(self) -> dict[str, str]:
        """Return document metadata."""

        return self._renderer.metadata()

    def go_to_page(
        self,
        page: int,
    ) -> None:
        """
        Navigate to a page.

        Args:
            page:
                Zero-based page index.

        Raises:
            ValueError:
                If the page number is outside the document.
        """

        if page < 0 or page >= self.page_count:
            raise ValueError(f"Invalid page number: {page}")

        self._current_page = page

    def next_page(self) -> bool:
        """
        Move to the next page.

        Returns:
            True if the page changed.
        """

        if self._current_page >= self.page_count - 1:
            return False

        self._current_page += 1

        return True

    def previous_page(self) -> bool:
        """
        Move to the previous page.

        Returns:
            True if the page changed.
        """

        if self._current_page <= 0:
            return False

        self._current_page -= 1

        return True

    def render_current_page(
        self,
        zoom: float = 1.0,
    ) -> QImage:
        """
        Render the current page.

        Args:
            zoom:
                Rendering zoom factor.

        Returns:
            Rendered page image.
        """

        return self._renderer.render_page(
            self._current_page,
            zoom=zoom,
        )

    @property
    def renderer(self) -> PdfRenderer:
        """Expose the underlying renderer."""

        return self._renderer
