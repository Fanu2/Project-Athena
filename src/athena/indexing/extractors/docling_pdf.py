"""
Docling-powered PDF extractor.
"""

from __future__ import annotations

from pathlib import Path

from docling.document_converter import DocumentConverter

from athena.indexing.exceptions import ExtractionError
from athena.indexing.extractors.base import BaseExtractor
from athena.indexing.models import ExtractedDocument, ExtractedPage


class DoclingPDFExtractor(BaseExtractor):
    """Extract PDF documents using Docling."""

    def __init__(self) -> None:
        """Initialize the Docling converter."""

        self._converter = DocumentConverter()

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        """Return supported file extensions."""

        return (".pdf",)

    def extract(
        self,
        document: Path,
    ) -> ExtractedDocument:
        """Extract text from a PDF document."""

        try:
            result = self._converter.convert(document)

            pages = tuple(
                ExtractedPage(
                    page_number=page.page_no,
                    text=result.document.export_to_text(
                        page_no=page.page_no,
                    ),
                )
                for page in result.document.pages.values()
            )

            return ExtractedDocument(
                document_id=document.name,
                path=document,
                title=document.stem,
                text=result.document.export_to_text(),
                pages=pages,
                page_count=len(pages),
            )

        except Exception as exc:
            raise ExtractionError(
                f"Failed to extract '{document.name}' using Docling.\n\n{type(exc).__name__}: {exc}"
            ) from exc
