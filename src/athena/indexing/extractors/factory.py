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

    _extractors: tuple[BaseExtractor, ...] = (
        PDFExtractor(),
        TextExtractor(),
        MarkdownExtractor(),
    )

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

        for extractor in cls._extractors:
            if extension in extractor.supported_extensions:
                return extractor

        raise UnsupportedDocumentError(f"Unsupported document type: {extension}")
