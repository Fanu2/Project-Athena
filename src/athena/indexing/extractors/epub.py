"""
EPUB document extractor.
"""

from __future__ import annotations

from pathlib import Path

from ebooklib import ITEM_DOCUMENT, epub

from athena.indexing.exceptions import ExtractionError
from athena.indexing.extractors.base import BaseExtractor
from athena.indexing.models import (
    ExtractedDocument,
    ExtractedPage,
)


class EPUBExtractor(BaseExtractor):
    """Extract text from EPUB documents."""

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        """Return supported extensions."""
        return (".epub",)

    def extract(
        self,
        document: Path,
    ) -> ExtractedDocument:
        """
        Extract text from an EPUB document.

        Args:
            document:
                Path to the EPUB file.

        Returns:
            ExtractedDocument.

        Raises:
            ExtractionError:
                If the EPUB cannot be read.
        """

        try:
            book = epub.read_epub(str(document))

            text_parts: list[str] = []

            from bs4 import BeautifulSoup

            for item in book.get_items():
                if item.get_type() == ITEM_DOCUMENT:
                    html = item.get_body_content().decode(
                        "utf-8",
                        errors="ignore",
                    )

                    soup = BeautifulSoup(html, "html.parser")
                    text = soup.get_text(separator="\n", strip=True)

                    if text:
                        text_parts.append(text)

        except Exception as exc:
            raise ExtractionError(f"Failed to extract '{document.name}'.") from exc

        pages = tuple(
            ExtractedPage(
                page_number=index + 1,
                text=text,
            )
            for index, text in enumerate(text_parts)
        )

        return ExtractedDocument(
            document_id=document.name,
            path=document,
            title=document.stem,
            text="\n\n".join(text_parts),
            pages=pages,
            page_count=len(pages),
        )
