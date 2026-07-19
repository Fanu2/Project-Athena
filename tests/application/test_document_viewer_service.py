"""
Tests for DocumentViewerService.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import fitz
import pytest
from PySide6.QtGui import QImage

from athena.application.viewer import DocumentViewerService
from athena.documents.models import Document


@pytest.fixture
def sample_pdf(tmp_path: Path) -> Path:
    pdf = tmp_path / "sample.pdf"

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Athena")
    doc.save(pdf)
    doc.close()

    return pdf


@pytest.fixture
def document(sample_pdf: Path) -> Document:
    now = datetime.now()

    return Document(
        id="doc-1",
        name="Sample",
        path=sample_pdf,
        size=sample_pdf.stat().st_size,
        created=now,
        modified=now,
    )


def test_open_document(document: Document) -> None:
    service = DocumentViewerService()

    service.open_document(document.path)

    assert service.is_open
    assert service.document_path == document.path
    assert service.current_page == 0
    assert service.page_count == 1


def test_close_document(document: Document) -> None:
    service = DocumentViewerService()

    service.open_document(document.path)
    service.close()

    assert not service.is_open
    assert service.document_path is None
    assert service.current_page == 0


def test_next_page_single_page(document: Document) -> None:
    service = DocumentViewerService()

    service.open_document(document.path)

    assert service.next_page() is False


def test_previous_page_first_page(document: Document) -> None:
    service = DocumentViewerService()

    service.open_document(document.path)

    assert service.previous_page() is False


def test_go_to_invalid_page(document: Document) -> None:
    service = DocumentViewerService()

    service.open_document(document.path)

    with pytest.raises(ValueError):
        service.go_to_page(10)


def test_render_current_page(document: Document) -> None:
    service = DocumentViewerService()

    service.open_document(document.path)

    image = service.render_current_page()

    assert isinstance(image, QImage)
    assert not image.isNull()


def test_metadata(document: Document) -> None:
    service = DocumentViewerService()

    service.open_document(document.path)

    metadata = service.metadata()

    assert isinstance(metadata, dict)
