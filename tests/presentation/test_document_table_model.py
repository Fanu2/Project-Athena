from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt

from athena.indexing.models import IndexedDocument
from athena.presentation.documents.document_table_model import (
    DocumentTableModel,
)


def create_document() -> IndexedDocument:
    return IndexedDocument(
        document_id="doc1",
        path=Path("sample.pdf"),
        title="Sample Document",
        sha256="abc123",
        page_count=10,
        indexed_at=datetime(2026, 1, 1, 12, 0),
    )


def test_row_count():
    model = DocumentTableModel(
        [
            create_document(),
        ]
    )

    assert model.rowCount() == 1


def test_column_count():
    model = DocumentTableModel()

    assert model.columnCount() == 4


def test_headers():
    model = DocumentTableModel()

    assert (
        model.headerData(
            0,
            Qt.Horizontal,
        )
        == "Title"
    )

    assert (
        model.headerData(
            1,
            Qt.Horizontal,
        )
        == "Pages"
    )

    assert (
        model.headerData(
            2,
            Qt.Horizontal,
        )
        == "Indexed"
    )

    assert (
        model.headerData(
            3,
            Qt.Horizontal,
        )
        == "Path"
    )


def test_data():
    model = DocumentTableModel(
        [
            create_document(),
        ]
    )

    index = model.index(
        0,
        0,
    )

    assert (
        model.data(
            index,
        )
        == "Sample Document"
    )


def test_set_documents():
    model = DocumentTableModel()

    assert model.rowCount() == 0

    model.set_documents(
        [
            create_document(),
        ]
    )

    assert model.rowCount() == 1


def test_document_at():
    document = create_document()

    model = DocumentTableModel(
        [
            document,
        ]
    )

    assert (
        model.document_at(
            0,
        )
        == document
    )
