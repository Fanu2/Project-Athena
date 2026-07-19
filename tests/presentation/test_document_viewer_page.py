"""
Tests for DocumentViewerPage.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import fitz
import pytest

from athena.application.viewer import DocumentViewerService
from athena.documents.models import Document
from athena.presentation.viewer import DocumentViewerPage


@pytest.fixture
def sample_pdf(tmp_path: Path) -> Path:
    """Create a one-page PDF."""

    pdf = tmp_path / "sample.pdf"

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Athena Viewer")
    doc.save(pdf)
    doc.close()

    return pdf


@pytest.fixture
def document(sample_pdf: Path) -> Document:
    """Create a test document."""

    now = datetime.now()

    return Document(
        id="doc-1",
        name="Sample",
        path=sample_pdf,
        size=sample_pdf.stat().st_size,
        created=now,
        modified=now,
    )


@pytest.fixture
def viewer_service() -> DocumentViewerService:
    """Create viewer service."""

    return DocumentViewerService()


def test_initial_state(qtbot) -> None:
    page = DocumentViewerPage()

    qtbot.addWidget(page)

    assert page.page_label.text() == "Page 0 / 0"
    assert page.status_label.text() == "No document loaded"
    assert not page.canvas.has_image


def test_attach_service(
    qtbot,
    viewer_service: DocumentViewerService,
) -> None:
    page = DocumentViewerPage()

    qtbot.addWidget(page)

    page.set_viewer_service(viewer_service)

    assert page.status_label.text() == "No document loaded"


def test_clear_service(
    qtbot,
    viewer_service: DocumentViewerService,
) -> None:
    page = DocumentViewerPage()

    qtbot.addWidget(page)

    page.set_viewer_service(viewer_service)

    page.clear_viewer_service()

    assert page.status_label.text() == "No document loaded"


def test_open_document(
    qtbot,
    viewer_service: DocumentViewerService,
    document: Document,
) -> None:
    page = DocumentViewerPage()

    qtbot.addWidget(page)

    page.set_viewer_service(viewer_service)

    page.open_document(document)

    assert page.canvas.has_image
    assert page.page_label.text() == "Page 1 / 1"
    assert page.status_label.text() == "Ready"


def test_navigation_single_page(
    qtbot,
    viewer_service: DocumentViewerService,
    document: Document,
) -> None:
    page = DocumentViewerPage()

    qtbot.addWidget(page)

    page.set_viewer_service(viewer_service)

    page.open_document(document)

    page.next_page()
    page.previous_page()

    assert page.page_label.text() == "Page 1 / 1"