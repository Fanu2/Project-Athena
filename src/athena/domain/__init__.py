"""
Athena domain models.
"""

from athena.domain.document import Document
from athena.domain.extracted_document import ExtractedDocument
from athena.domain.extracted_page import ExtractedPage

__all__ = [
    "Document",
    "ExtractedDocument",
    "ExtractedPage",
]