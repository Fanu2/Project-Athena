"""
HTML document extractor.
"""

from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup

from athena.indexing.extractors.base import BaseExtractor
from athena.indexing.models import (
    ExtractedDocument,
    ExtractedPage,
)


class HTMLExtractor(BaseExtractor):
    """Extract text from HTML documents."""

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        """Return supported extensions."""

        return (
            ".html",
            ".htm",
        )

    def extract(
        self,
        document: Path,
    ) -> ExtractedDocument:
        """
        Extract visible text from HTML.

        Args:
            document:
                HTML document path.

        Returns:
            ExtractedDocument.
        """

        html = document.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        for tag in soup(
            [
                "script",
                "style",
            ]
        ):
            tag.decompose()

        text = soup.get_text(
            separator="\n",
            strip=True,
        )

        return ExtractedDocument(
            document_id=document.name,
            path=document,
            title=(
                soup.title.string.strip()
                if soup.title and soup.title.string
                else document.stem
            ),
            text=text,
            pages=(
                ExtractedPage(
                    page_number=1,
                    text=text,
                ),
            ),
            page_count=1,
        )
