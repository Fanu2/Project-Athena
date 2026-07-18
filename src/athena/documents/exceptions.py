"""
Document exceptions.
"""


class DocumentError(Exception):
    """Base document exception."""


class InvalidDocumentError(DocumentError):
    """Raised when a document fails validation."""
