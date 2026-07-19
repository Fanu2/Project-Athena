"""
Viewer exceptions.

Defines exceptions used by the document viewer infrastructure.
These exceptions isolate the rest of Athena from PyMuPDF-specific
errors and provide a stable API for higher layers.
"""

from __future__ import annotations


class ViewerError(Exception):
    """Base exception for all viewer-related errors."""


class DocumentOpenError(ViewerError):
    """Raised when a document cannot be opened."""


class InvalidPageError(ViewerError):
    """Raised when an invalid page number is requested."""


class UnsupportedDocumentError(ViewerError):
    """Raised when the document format is unsupported."""
