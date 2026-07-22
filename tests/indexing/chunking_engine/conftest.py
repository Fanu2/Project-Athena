"""
Shared pytest fixtures for the chunking engine tests.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from athena.indexing.models import (
    BlockType,
    ChunkCandidate,
    ChunkType,
    DocumentBlock,
    DocumentChunk,
    ExtractedDocument,
    ExtractedPage,
)


@pytest.fixture
def empty_document() -> ExtractedDocument:
    """An empty extracted document."""

    return ExtractedDocument(
        document_id="doc-empty",
        path=Path("empty.txt"),
        title="Empty Document",
        text="",
        pages=(),
        page_count=0,
    )


@pytest.fixture
def sample_document() -> ExtractedDocument:
    """A simple single-page document."""

    text = (
        "# Introduction\n\n"
        "Athena is a local-first research assistant.\n\n"
        "It uses structure-aware chunking."
    )

    page = ExtractedPage(
        page_number=1,
        text=text,
    )

    return ExtractedDocument(
        document_id="doc-001",
        path=Path("sample.md"),
        title="Sample Document",
        text=text,
        pages=(page,),
        page_count=1,
    )


@pytest.fixture
def multi_page_document() -> ExtractedDocument:
    """A two-page document."""

    page1 = ExtractedPage(
        page_number=1,
        text="# Page One\n\nFirst page.",
    )

    page2 = ExtractedPage(
        page_number=2,
        text="# Page Two\n\nSecond page.",
    )

    return ExtractedDocument(
        document_id="doc-002",
        path=Path("multipage.pdf"),
        title="Multi Page",
        text=f"{page1.text}\n\n{page2.text}",
        pages=(page1, page2),
        page_count=2,
    )


@pytest.fixture
def long_document() -> ExtractedDocument:
    """Document containing a long paragraph."""

    paragraph = "Athena " * 400

    page = ExtractedPage(
        page_number=1,
        text=paragraph,
    )

    return ExtractedDocument(
        document_id="doc-long",
        path=Path("long.txt"),
        title="Long Document",
        text=paragraph,
        pages=(page,),
        page_count=1,
    )


@pytest.fixture
def sample_block() -> DocumentBlock:
    """A simple paragraph block."""

    return DocumentBlock(
        block_type=BlockType.PARAGRAPH,
        text="Athena is amazing.",
        page_number=1,
        start_offset=0,
        end_offset=18,
    )


@pytest.fixture
def heading_block() -> DocumentBlock:
    """A heading block."""

    return DocumentBlock(
        block_type=BlockType.HEADING,
        text="Introduction",
        page_number=1,
        start_offset=0,
        end_offset=12,
        heading="Introduction",
        heading_path=("Introduction",),
    )


@pytest.fixture
def sample_candidate(
    sample_block: DocumentBlock,
) -> ChunkCandidate:
    """A ChunkCandidate containing one paragraph."""

    return ChunkCandidate(
        blocks=[sample_block],
        text=sample_block.text,
        page_number=1,
        heading=None,
        heading_path=(),
        chunk_type=ChunkType.PARAGRAPH,
    )


@pytest.fixture
def sample_chunk() -> DocumentChunk:
    """A completed DocumentChunk."""

    return DocumentChunk(
        chunk_id="chunk-001",
        document_id="doc-001",
        chunk_index=0,
        page_number=1,
        start_offset=0,
        end_offset=18,
        text="Athena is amazing.",
        heading=None,
        heading_path=(),
        chunk_type=ChunkType.PARAGRAPH,
        previous_chunk=None,
        next_chunk=None,
    )