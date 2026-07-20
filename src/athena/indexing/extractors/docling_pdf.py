"""
Docling-powered PDF extractor.
"""

from __future__ import annotations

from pathlib import Path

from docling.document_converter import DocumentConverter

from athena.indexing.exceptions import ExtractionError
from athena.indexing.extractors.base import BaseExtractor
from athena.indexing.models import ExtractedDocument


class DoclingPDFExtractor(BaseExtractor):
    """Extract PDF documents using Docling."""

    def __init__(self) -> None:
        self._converter = DocumentConverter()

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        return (".pdf",)

    def extract(
        self,
        document: Path,
    ) -> ExtractedDocument:
        """Extract text from a PDF document."""

        try:
            result = self._converter.convert(document)

            return ExtractedDocument(
                document_id=document.name,
                path=document,
                title=document.stem,
                text=result.document.export_to_markdown(),
                page_count=len(result.document.pages),
            )

        except Exception as exc:
            raise ExtractionError(
                f"Failed to extract '{document.name}' using Docling."
            ) from exc