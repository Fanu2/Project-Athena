"""
Extracted document domain model.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from athena.domain.extracted_page import ExtractedPage


@dataclass(slots=True)
class ExtractedDocument:
    """Represents the extracted contents of a document."""

    title: str = ""

    author: str = ""

    pages: list[ExtractedPage] = field(default_factory=list)

    metadata: dict[str, str] = field(default_factory=dict)

    @property
    def text(self) -> str:
        """Return the full document text."""
        return "\n\n".join(page.text for page in self.pages)

    @property
    def page_count(self) -> int:
        """Return the number of extracted pages."""
        return len(self.pages)

    def add_page(
        self,
        page: ExtractedPage,
    ) -> None:
        """Add a page to the document."""
        self.pages.append(page)
