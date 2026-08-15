"""
Calibre import dialog.

Allows users to select books from
a Calibre library.
"""

from pathlib import Path

from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from athena.knowledge.acquisition.providers.calibre_library import (
    CalibreLibraryReader,
)


class CalibreDialog(QDialog):
    """
    Select books from a Calibre library.
    """

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        """Initialize dialog."""

        super().__init__(parent)

        self.setWindowTitle(
            "Import from Calibre"
        )

        self.resize(
            600,
            450,
        )

        self._library_path: Path | None = None

        self._books: list[dict] = []

        self.library_label = QLabel(
            "No Calibre library selected",
        )

        self.book_list = QListWidget()

        self.select_button = QPushButton(
            "Select Calibre Library",
        )

        self.ok_button = QPushButton(
            "Import Selected",
        )

        self.ok_button.setEnabled(
            False,
        )

        self._setup_ui()

        self._connect_signals()

    def _setup_ui(self) -> None:
        """Build dialog layout."""

        layout = QVBoxLayout(self)

        layout.addWidget(
            self.select_button,
        )

        layout.addWidget(
            self.library_label,
        )

        layout.addWidget(
            self.book_list,
        )

        layout.addWidget(
            self.ok_button,
        )

        self.setLayout(
            layout,
        )

    def _connect_signals(self) -> None:
        """Connect button events."""

        self.select_button.clicked.connect(
            self.select_library,
        )

        self.ok_button.clicked.connect(
            self.accept,
        )

    def select_library(self) -> None:
        """
        Select and load a Calibre library.
        """

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Calibre Library Folder",
            str(Path.home()),
            QFileDialog.Option.ShowDirsOnly,
        )

        if not folder:
            return

        library_path = Path(folder)

        reader = CalibreLibraryReader(
            library_path,
        )

        if not reader.exists():

            QMessageBox.warning(
                self,
                "Invalid Calibre Library",
                (
                    "This is not a Calibre library.\n\n"
                    "Please select the folder containing "
                    "metadata.db."
                ),
            )

            return

        try:
            books = reader.list_books()

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Calibre Error",
                str(exc),
            )

            return

        if not books:

            QMessageBox.information(
                self,
                "Empty Library",
                "No books were found in this Calibre library.",
            )

            return

        self._library_path = library_path

        self._books = books

        self.library_label.setText(
            f"Library: {library_path}\n"
            f"Books found: {len(books)}"
        )

        self.book_list.clear()

        for book in books:

            label = book.get(
                "title",
                "Unknown title",
            )

            self.book_list.addItem(
                label,
            )

        self.ok_button.setEnabled(
            True,
        )

    def selected_book_ids(self) -> list[int]:
        """
        Return selected Calibre book IDs.
        """

        return [
            self._books[index.row()]["id"]
            for index in self.book_list.selectedIndexes()
        ]

    @property
    def library_path(self) -> Path | None:
        """
        Return selected Calibre library path.
        """

        return self._library_path