"""
Core data models for the Athena Chunking Engine.

These models define the data flow through the chunking pipeline:

ExtractedDocument
        ↓
DocumentBlock
        ↓
ChunkCandidate
        ↓
DocumentChunk
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path


# ============================================================================
# Extracted Document Models
# ============================================================================


@dataclass(slots=True, frozen=True)
class ExtractedPage:
    """Text extracted from a single page."""

    page_number: int
    text: str


@dataclass(slots=True, frozen=True)
class ExtractedDocument:
    """Represents a fully extracted document."""

    document_id: str
    path: Path
    title: str
    text: str
    pages: tuple[ExtractedPage, ...]
    page_count: int


# ============================================================================
# Structural Models
# ============================================================================


class BlockType(str, Enum):
    """Logical document block type."""

    HEADING = "heading"
    PARAGRAPH = "paragraph"
    LIST = "list"
    TABLE = "table"
    CODE = "code"


class ChunkType(str, Enum):
    """Final chunk classification."""

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    LIST = "list"
    TABLE = "table"
    CODE = "code"
    MIXED = "mixed"


@dataclass(slots=True, frozen=True)
class DocumentBlock:
    """
    Smallest structural unit produced by the parser.
    """

    block_type: BlockType

    text: str

    page_number: int

    start_offset: int

    end_offset: int

    heading: str | None = None

    heading_path: tuple[str, ...] = ()


# ============================================================================
# Chunk Assembly
# ============================================================================


@dataclass(slots=True)
class ChunkCandidate:
    """
    Mutable chunk under construction.

    Produced by ChunkBuilder before metadata enrichment.
    """

    blocks: list[DocumentBlock] = field(default_factory=list)

    text: str = ""

    page_number: int = 1

    heading: str | None = None

    heading_path: tuple[str, ...] = ()

    chunk_type: ChunkType = ChunkType.PARAGRAPH


# ============================================================================
# Final Searchable Chunk
# ============================================================================


@dataclass(slots=True, frozen=True)
class DocumentChunk:
    """
    Final chunk stored in the vector index.
    """

    chunk_id: str

    document_id: str

    chunk_index: int

    page_number: int

    start_offset: int

    end_offset: int

    text: str

    heading: str | None = None

    heading_path: tuple[str, ...] = ()

    chunk_type: ChunkType = ChunkType.PARAGRAPH

    previous_chunk: str | None = None

    next_chunk: str | None = None


# ============================================================================
# Indexed Document
# ============================================================================


@dataclass(slots=True, frozen=True)
class IndexedDocument:
    """Metadata describing an indexed document."""

    document_id: str

    path: Path

    title: str

    sha256: str

    page_count: int

    indexed_at: datetime
