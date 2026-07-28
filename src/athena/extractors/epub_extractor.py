"""
EPUB document extractor.
"""

from __future__ import annotations

from pathlib import Path

from ebooklib import epub, ITEM_DOCUMENT

from athena.indexing.exceptions import ExtractionError
from athena.indexing.extractors.base import BaseExtractor
from athena.indexing.models import ExtractedDocument


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
        """

        try:
            book = epub.read_epub(str(document))

            parts: list[str] = []

            for item in book.get_items():
                if item.get_type() == ITEM_DOCUMENT:
                    content = item.get_body_content().decode(
                        "utf-8",
                        errors="ignore",
                    )

                    try:
                        from bs4 import BeautifulSoup

                        soup = BeautifulSoup(content, "html.parser")
                        text = soup.get_text(separator="\n")
                    except Exception:
                        text = content

                    parts.append(text)

        except Exception as exc:
            raise ExtractionError(f"Failed to extract '{document.name}'.") from exc

        return ExtractedDocument(
            document_id=document.name,
            path=document,
            title=document.stem,
            text="\n\n".join(parts),
            page_count=len(parts),
        )

