"""
Tests for PdfRenderer.
"""

from __future__ import annotations

from pathlib import Path

import fitz
import pytest
from PySide6.QtCore import QSize
from PySide6.QtGui import QImage

from athena.infrastructure.viewer import (
    DocumentOpenError,
    InvalidPageError,
    PdfRenderer,
    UnsupportedDocumentError,
)


@pytest.fixture
def sample_pdf(tmp_path: Path) -> Path:
    """Create a one-page PDF for testing."""

    pdf_path = tmp_path / "sample.pdf"

    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Hello Athena")
    document.save(pdf_path)
    document.close()

    return pdf_path


@pytest.fixture
def text_file(tmp_path: Path) -> Path:
    """Create a plain text file."""

    path = tmp_path / "sample.txt"
    path.write_text("Not a PDF", encoding="utf-8")
    return path


def test_open_pdf(sample_pdf: Path) -> None:
    renderer = PdfRenderer()

    renderer.open(sample_pdf)

    assert renderer.is_open
    assert renderer.path == sample_pdf
    assert renderer.page_count == 1


def test_close_pdf(sample_pdf: Path) -> None:
    renderer = PdfRenderer()

    renderer.open(sample_pdf)
    renderer.close()

    assert not renderer.is_open
    assert renderer.path is None


def test_open_missing_pdf() -> None:
    renderer = PdfRenderer()

    with pytest.raises(DocumentOpenError):
        renderer.open(Path("does_not_exist.pdf"))


def test_open_non_pdf(text_file: Path) -> None:
    renderer = PdfRenderer()

    with pytest.raises(UnsupportedDocumentError):
        renderer.open(text_file)


def test_page_size(sample_pdf: Path) -> None:
    renderer = PdfRenderer()
    renderer.open(sample_pdf)

    size = renderer.page_size(0)

    assert isinstance(size, QSize)
    assert size.width() > 0
    assert size.height() > 0


def test_render_page(sample_pdf: Path) -> None:
    renderer = PdfRenderer()
    renderer.open(sample_pdf)

    image = renderer.render_page(0)

    assert isinstance(image, QImage)
    assert not image.isNull()


def test_invalid_page(sample_pdf: Path) -> None:
    renderer = PdfRenderer()
    renderer.open(sample_pdf)

    with pytest.raises(InvalidPageError):
        renderer.render_page(5)


def test_metadata(sample_pdf: Path) -> None:
    renderer = PdfRenderer()
    renderer.open(sample_pdf)

    metadata = renderer.metadata()

    assert isinstance(metadata, dict)
    assert "title" in metadata
    assert "author" in metadata


def test_context_manager(sample_pdf: Path) -> None:
    with PdfRenderer() as renderer:
        renderer.open(sample_pdf)
        assert renderer.is_open

    assert not renderer.is_open
