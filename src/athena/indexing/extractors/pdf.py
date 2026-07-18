"""
PDF document extractor.
"""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import fitz

from athena.indexing.exceptions import ExtractionError
from athena.indexing.extractors.base import BaseExtractor
from athena.indexing.models import ExtractedDocument


class PDFExtractor(BaseExtractor):
    """Extract text from PDF documents."""

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        """Return supported file extensions."""

        return (".pdf",)

    def extract(
        self,
        document: Path,
    ) -> ExtractedDocument:
        """
        Extract text from a PDF document.

        Args:
            document:
                Path to the PDF.

        Returns:
            ExtractedDocument.

        Raises:
            ExtractionError:
                If the PDF cannot be read.
        """

        try:
            pdf = fitz.open(document)

            pages: list[str] = []

            for page in pdf:
                pages.append(page.get_text())

            pdf.close()

        except Exception as exc:
            raise ExtractionError(f"Failed to extract '{document.name}'.") from exc

        return ExtractedDocument(
            document_id=str(uuid4()),
            path=document,
            title=document.stem,
            text="\n".join(pages),
            page_count=len(pages),
        )
