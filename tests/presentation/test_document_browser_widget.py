from athena.presentation.documents.document_browser_widget import (
    DocumentBrowserWidget,
)


def test_widget_creation(qtbot):
    widget = DocumentBrowserWidget()

    qtbot.addWidget(widget)

    assert widget.model is not None
    assert widget.table is not None
    assert widget.search_box is not None


def test_search_placeholder(qtbot):
    widget = DocumentBrowserWidget()

    qtbot.addWidget(widget)

    assert widget.search_box.placeholderText() == "Search documents..."


def test_table_model(qtbot):
    widget = DocumentBrowserWidget()

    qtbot.addWidget(widget)

    assert widget.table.model() is widget.model
