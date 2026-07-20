"""
Indexing models.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(slots=True, frozen=True)
class ExtractedPage:
    """Text extracted from a single document page."""

    page_number: int

    text: str


@dataclass(slots=True, frozen=True)
class ExtractedDocument:
    """Document after text extraction."""

    document_id: str

    path: Path

    title: str

    # Complete extracted document text.
    text: str

    # Page-by-page extracted content.
    pages: tuple[ExtractedPage, ...]

    page_count: int


@dataclass(slots=True, frozen=True)
class DocumentChunk:
    """A searchable chunk of text."""

    chunk_id: str

    document_id: str

    chunk_index: int

    page_number: int

    # Character offsets within the page.
    start_offset: int

    end_offset: int

    text: str


@dataclass(slots=True, frozen=True)
class IndexedDocument:
    """Metadata for an indexed document."""

    document_id: str

    path: Path

    title: str

    sha256: str

    page_count: int

    indexed_at: datetime