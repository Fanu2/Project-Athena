"""
Plain text document extractor.
"""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from athena.indexing.extractors.base import BaseExtractor
from athena.indexing.models import ExtractedDocument


class TextExtractor(BaseExtractor):
    """Extract text from plain text documents."""

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        """Return supported file extensions."""

        return (".txt",)

    def extract(
        self,
        document: Path,
    ) -> ExtractedDocument:
        """
        Extract text from a plain text file.

        Args:
            document:
                Path to the text document.

        Returns:
            ExtractedDocument.
        """

        text = document.read_text(
            encoding="utf-8",
        )

        return ExtractedDocument(
            document_id=str(uuid4()),
            path=document,
            title=document.stem,
            text=text,
            page_count=1,
        )
