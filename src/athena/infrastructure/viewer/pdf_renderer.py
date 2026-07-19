"""
PDF renderer.

Provides low-level PDF rendering using PyMuPDF.

This class is responsible only for opening PDF documents and
rendering pages as QImage objects. It contains no UI logic and
is intended to be used by DocumentViewerService.
"""

from __future__ import annotations

from pathlib import Path

import fitz  # PyMuPDF
from PySide6.QtCore import QSize
from PySide6.QtGui import QImage

from .exceptions import (
    DocumentOpenError,
    InvalidPageError,
    UnsupportedDocumentError,
)


class PdfRenderer:
    """Low-level PDF renderer."""

    def __init__(self) -> None:
        """Initialize the renderer."""

        self._document: fitz.Document | None = None
        self._path: Path | None = None

    @property
    def path(self) -> Path | None:
        """Return the currently opened document path."""

        return self._path

    @property
    def is_open(self) -> bool:
        """Return True if a document is currently open."""

        return self._document is not None

    def open(
        self,
        path: Path,
    ) -> None:
        """
        Open a PDF document.

        Args:
            path:
                PDF document path.

        Raises:
            DocumentOpenError:
                If the document cannot be opened.

            UnsupportedDocumentError:
                If the file is not a supported PDF.
        """

        self.close()

        if not path.exists():
            raise DocumentOpenError(f"Document does not exist: {path}")

        if path.suffix.lower() != ".pdf":
            raise UnsupportedDocumentError(f"Unsupported document type: {path.suffix}")

        try:
            self._document = fitz.open(path)
            self._path = path

        except Exception as exc:
            raise DocumentOpenError(f"Unable to open PDF: {path}") from exc

    def close(self) -> None:
        """Close the current document."""

        if self._document is not None:
            self._document.close()

        self._document = None
        self._path = None

    def _require_document(self) -> fitz.Document:
        """
        Return the current document.

        Raises:
            DocumentOpenError:
                If no document is open.
        """

        if self._document is None:
            raise DocumentOpenError("No document is currently open.")

        return self._document

    @property
    def page_count(self) -> int:
        """Return total number of pages."""

        document = self._require_document()

        return int(document.page_count)

    def metadata(self) -> dict[str, str]:
        """
        Return PDF metadata.

        Returns:
            Dictionary containing document metadata.
        """

        document = self._require_document()

        metadata = document.metadata or {}

        return {
            "title": metadata.get("title", ""),
            "author": metadata.get("author", ""),
            "subject": metadata.get("subject", ""),
            "creator": metadata.get("creator", ""),
            "producer": metadata.get("producer", ""),
        }

    def page_size(
        self,
        page_number: int,
    ) -> QSize:
        """
        Return page size.

        Args:
            page_number:
                Zero-based page index.

        Raises:
            InvalidPageError:
                If page is outside the document.
        """

        document = self._require_document()

        if page_number < 0 or page_number >= document.page_count:
            raise InvalidPageError(f"Invalid page number: {page_number}")

        page = document.load_page(page_number)

        rect = page.rect

        return QSize(
            int(rect.width),
            int(rect.height),
        )

    def render_page(
        self,
        page_number: int,
        zoom: float = 1.0,
    ) -> QImage:
        """
        Render a PDF page.

        Args:
            page_number:
                Zero-based page number.

            zoom:
                Rendering zoom factor.

        Returns:
            Rendered page as a QImage.

        Raises:
            InvalidPageError:
                If the page number is invalid.
        """

        document = self._require_document()

        if page_number < 0 or page_number >= document.page_count:
            raise InvalidPageError(f"Invalid page number: {page_number}")

        page = document.load_page(page_number)

        matrix = fitz.Matrix(
            zoom,
            zoom,
        )

        pixmap = page.get_pixmap(
            matrix=matrix,
            alpha=False,
        )

        image = QImage(
            pixmap.samples,
            pixmap.width,
            pixmap.height,
            pixmap.stride,
            QImage.Format.Format_RGB888,
        )

        # Detach from PyMuPDF memory.
        return image.copy()

    @property
    def title(self) -> str:
        """Return the document title."""

        return self.metadata()["title"]

    @property
    def author(self) -> str:
        """Return the document author."""

        return self.metadata()["author"]

    @property
    def subject(self) -> str:
        """Return the document subject."""

        return self.metadata()["subject"]

    @property
    def creator(self) -> str:
        """Return the application that created the document."""

        return self.metadata()["creator"]

    @property
    def producer(self) -> str:
        """Return the PDF producer."""

        return self.metadata()["producer"]

    def __enter__(self) -> "PdfRenderer":
        """Support context manager usage."""

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        """Close the document when leaving a context."""

        self.close()
