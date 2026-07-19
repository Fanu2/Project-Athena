"""
PDF viewer infrastructure.

This package contains the low-level rendering components used by
Athena's Document Viewer.
"""

from .exceptions import (
    DocumentOpenError,
    InvalidPageError,
    UnsupportedDocumentError,
    ViewerError,
)
from .pdf_renderer import PdfRenderer

__all__ = [
    "PdfRenderer",
    "ViewerError",
    "DocumentOpenError",
    "InvalidPageError",
    "UnsupportedDocumentError",
]
