"""
Markdown document extractor.
"""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from athena.indexing.extractors.base import BaseExtractor
from athena.indexing.models import ExtractedDocument


class MarkdownExtractor(BaseExtractor):
    """Extract text from Markdown documents."""

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        """Return supported file extensions."""

        return (".md",)

    def extract(
        self,
        document: Path,
    ) -> ExtractedDocument:
        """
        Extract text from a Markdown document.

        Args:
            document:
                Path to the Markdown document.

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
