"""
Indexing models.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(slots=True, frozen=True)
class ExtractedDocument:
    """Document after text extraction."""

    document_id: str

    path: Path

    title: str

    text: str

    page_count: int


@dataclass(slots=True, frozen=True)
class DocumentChunk:
    """A searchable chunk of text."""

    chunk_id: str

    document_id: str

    chunk_index: int

    page_number: int

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
