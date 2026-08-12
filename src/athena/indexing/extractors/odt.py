"""
OpenDocument Text (.odt) document extractor.
"""

from __future__ import annotations

from pathlib import Path

from odf import text
from odf.opendocument import load
from odf.teletype import extractText

from athena.indexing.extractors.base import BaseExtractor
from athena.indexing.models import (
    ExtractedDocument,
    ExtractedPage,
)


class ODTExtractor(BaseExtractor):
    """Extract text from OpenDocument Text files."""

    @property
    def supported_extensions(
        self,
    ) -> tuple[str, ...]:
        """
        Return supported file extensions.
        """

        return (".odt",)

    def extract(
        self,
        document: Path,
    ) -> ExtractedDocument:
        """
        Extract text from an ODT document.

        Args:
            document:
                Path to the ODT document.

        Returns:
            ExtractedDocument.
        """

        odt_document = load(
            str(document),
        )

        paragraphs = odt_document.getElementsByType(
            text.P,
        )

        extracted_text = "\n".join(
            extractText(paragraph).strip()
            for paragraph in paragraphs
            if extractText(paragraph).strip()
        )

        return ExtractedDocument(
            document_id=document.name,
            path=document,
            title=document.stem,
            text=extracted_text,
            pages=(
                ExtractedPage(
                    page_number=1,
                    text=extracted_text,
                ),
            ),
            page_count=1,
        )
