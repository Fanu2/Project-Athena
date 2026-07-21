"""
Document extractor factory.
"""

from __future__ import annotations

from pathlib import Path

from athena.indexing.exceptions import (
    UnsupportedDocumentError,
)
from athena.indexing.extractors.base import (
    BaseExtractor,
)
from athena.indexing.extractors.docling_pdf import (
    DoclingPDFExtractor,
)
from athena.indexing.extractors.docx import (
    DOCXExtractor,
)
from athena.indexing.extractors.markdown import (
    MarkdownExtractor,
)
from athena.indexing.extractors.pdf import (
    PDFExtractor,
)
from athena.indexing.extractors.text import (
    TextExtractor,
)


class ExtractorFactory:
    """Factory for document extractors."""

    # Toggle between the legacy PDF extractor and Docling.
    # Set to True to enable Docling.
    USE_DOCLING = True

    @classmethod
    def _pdf_extractor(cls) -> BaseExtractor:
        """Return the configured PDF extractor."""
        if cls.USE_DOCLING:
            return DoclingPDFExtractor()
        return PDFExtractor()

    @classmethod
    def get_extractor(
        cls,
        document: Path,
    ) -> BaseExtractor:
        """
        Return an extractor for a document.

        Args:
            document:
                Document path.

        Returns:
            Matching extractor.

        Raises:
            UnsupportedDocumentError:
                If no extractor supports the file.
        """

        extension = document.suffix.lower()

        extractors: tuple[BaseExtractor, ...] = (
            cls._pdf_extractor(),
            TextExtractor(),
            MarkdownExtractor(),
            DOCXExtractor(),
        )

        for extractor in extractors:
            if extension in extractor.supported_extensions:
                return extractor

        raise UnsupportedDocumentError(f"Unsupported document type: {extension}")
