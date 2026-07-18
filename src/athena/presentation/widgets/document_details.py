"""
Document details widget.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QLabel,
    QFormLayout,
    QPushButton,
    QTextEdit,
    QWidget,
)

from athena.bookmarks.service import BookmarkService
from athena.documents.models import Document
from athena.notes.service import NoteService


class DocumentDetails(QWidget):
    """Displays selected document information."""

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._document: Document | None = None

        self._bookmark_service: BookmarkService | None = None

        self._note_service: NoteService | None = None

        self.name_label = QLabel("-")
        self.path_label = QLabel("-")
        self.size_label = QLabel("-")
        self.created_label = QLabel("-")
        self.modified_label = QLabel("-")

        self.bookmark_button = QPushButton(
            "☆ Bookmark",
        )

        self.notes_editor = QTextEdit()

        self.notes_editor.setPlaceholderText(
            "Write research notes...",
        )

        self.save_note_button = QPushButton(
            "Save Note",
        )

        self.delete_note_button = QPushButton(
            "Delete Note",
        )

        self.bookmark_button.setEnabled(False)
        self.save_note_button.setEnabled(False)
        self.delete_note_button.setEnabled(False)

        self._setup_ui()

        self.bookmark_button.clicked.connect(
            self._toggle_bookmark,
        )

        self.save_note_button.clicked.connect(
            self._save_note,
        )

        self.delete_note_button.clicked.connect(
            self._delete_note,
        )

    def _setup_ui(self) -> None:
        """Create layout."""

        layout = QFormLayout(self)

        layout.addRow(
            "Name:",
            self.name_label,
        )

        layout.addRow(
            "Path:",
            self.path_label,
        )

        layout.addRow(
            "Size:",
            self.size_label,
        )

        layout.addRow(
            "Created:",
            self.created_label,
        )

        layout.addRow(
            "Modified:",
            self.modified_label,
        )

        layout.addRow(
            "",
            self.bookmark_button,
        )

        layout.addRow(
            "Research Notes:",
            self.notes_editor,
        )

        layout.addRow(
            "",
            self.save_note_button,
        )

        layout.addRow(
            "",
            self.delete_note_button,
        )

    def set_bookmark_service(
        self,
        service: BookmarkService,
    ) -> None:
        """Attach bookmark service."""

        self._bookmark_service = service

    def set_note_service(
        self,
        service: NoteService,
    ) -> None:
        """Attach note service."""

        self._note_service = service

    def show_document(
        self,
        document: Document,
    ) -> None:
        """Display document information."""

        self._document = document

        self.name_label.setText(
            document.name,
        )

        self.path_label.setText(
            str(document.path),
        )

        self.size_label.setText(
            f"{document.size / 1024:.1f} KB",
        )

        self.created_label.setText(
            document.created.strftime(
                "%Y-%m-%d %H:%M",
            ),
        )

        self.modified_label.setText(
            document.modified.strftime(
                "%Y-%m-%d %H:%M",
            ),
        )

        self._update_bookmark_state()
        self._load_note_state()

    def _toggle_bookmark(self) -> None:
        """Toggle bookmark state."""

        if self._document is None:
            return

        if self._bookmark_service is None:
            return

        document_id = self._document.id

        if self._bookmark_service.is_bookmarked(
            document_id,
        ):
            self._bookmark_service.remove(
                document_id,
            )
        else:
            self._bookmark_service.add(
                document_id,
            )

        self._update_bookmark_state()

    def _update_bookmark_state(self) -> None:
        """Update button text."""

        if self._document is None:
            self.bookmark_button.setEnabled(False)
            return

        if self._bookmark_service is None:
            self.bookmark_button.setEnabled(False)
            return

        self.bookmark_button.setEnabled(True)

        if self._bookmark_service.is_bookmarked(
            self._document.id,
        ):
            self.bookmark_button.setText(
                "★ Bookmarked",
            )
        else:
            self.bookmark_button.setText(
                "☆ Bookmark",
            )

    def _load_note_state(self) -> None:
        """Load document note."""

        if self._document is None:
            return

        if self._note_service is None:
            return

        note = self._note_service.get(
            self._document.id,
        )

        if note is None:
            self.notes_editor.clear()
        else:
            self.notes_editor.setText(
                note.content,
            )

        self.save_note_button.setEnabled(True)
        self.delete_note_button.setEnabled(
            note is not None,
        )

    def _save_note(self) -> None:
        """Save document note."""

        if self._document is None:
            return

        if self._note_service is None:
            return

        self._note_service.create(
            self._document.id,
            self.notes_editor.toPlainText(),
        )

        self._load_note_state()

    def _delete_note(self) -> None:
        """Delete document note."""

        if self._document is None:
            return

        if self._note_service is None:
            return

        self._note_service.delete(
            self._document.id,
        )

        self.notes_editor.clear()

        self._load_note_state()

    def clear(self) -> None:
        """Clear document information."""

        self._document = None

        self.name_label.setText("-")
        self.path_label.setText("-")
        self.size_label.setText("-")
        self.created_label.setText("-")
        self.modified_label.setText("-")

        self.notes_editor.clear()

        self.bookmark_button.setEnabled(False)
        self.save_note_button.setEnabled(False)
        self.delete_note_button.setEnabled(False)

        self.bookmark_button.setText(
            "☆ Bookmark",
        )
