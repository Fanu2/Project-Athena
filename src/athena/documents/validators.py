"""
Document validators.
"""

from __future__ import annotations

from pathlib import Path

from athena.documents.constants import (
    SUPPORTED_DOCUMENT_TYPES,
)
from athena.documents.exceptions import (
    InvalidDocumentError,
)


def validate_document(path: Path) -> Path:
    """
    Validate a document before importing.

    Args:
        path:
            Path to the document.

    Returns:
        The validated document path.

    Raises:
        InvalidDocumentError:
            If the document does not exist, is not a file,
            or has an unsupported file type.
    """

    if not path.exists():
        raise InvalidDocumentError("Document does not exist.")

    if not path.is_file():
        raise InvalidDocumentError("Path is not a file.")

    suffix = path.suffix.lower()

    if suffix not in SUPPORTED_DOCUMENT_TYPES:
        supported = ", ".join(SUPPORTED_DOCUMENT_TYPES)

        raise InvalidDocumentError(f"Unsupported document type. " f"Supported types: {supported}")

    return path
