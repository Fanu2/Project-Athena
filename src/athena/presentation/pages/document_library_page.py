"""
Document library page.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QLabel,
    QInputDialog,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from athena.bookmarks.service import BookmarkService
from athena.documents.models import Document
from athena.notes.service import NoteService

from athena.presentation.widgets.collections_widget import (
    CollectionsWidget,
)

from athena.presentation.widgets.document_details import (
    DocumentDetails,
)

from athena.presentation.widgets.document_table import (
    DocumentTable,
)

from athena.presentation.widgets.document_toolbar import (
    DocumentToolbar,
)

from athena.services.workspace_document_service import (
    WorkspaceDocumentService,
)

from athena.workspace.collections.service import (
    CollectionService,
)


class DocumentLibraryPage(QWidget):
    """Workspace document library."""

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self._document_service: WorkspaceDocumentService | None = None
        self._bookmark_service: BookmarkService | None = None
        self._note_service: NoteService | None = None
        self._collection_service: CollectionService | None = None

        self.toolbar = DocumentToolbar()

        self.collections = CollectionsWidget()

        self.table = DocumentTable()

        self.details = DocumentDetails()

        self.status_label = QLabel()

        self._setup_ui()

        self.table.table.itemSelectionChanged.connect(
            self._on_document_selected,
        )

        self.collections.collection_selected.connect(
            self._on_collection_selected,
        )

        self.toolbar.add_collection_button.clicked.connect(
            self.add_selected_document_to_collection,
        )

        self.clear_document_service()

    def _setup_ui(self) -> None:
        """Configure the page layout."""

        layout = QVBoxLayout(self)

        layout.addWidget(
            self.toolbar,
        )

        main_splitter = QSplitter()

        document_splitter = QSplitter()

        document_splitter.addWidget(
            self.table,
        )

        document_splitter.addWidget(
            self.details,
        )

        main_splitter.addWidget(
            self.collections,
        )

        main_splitter.addWidget(
            document_splitter,
        )

        main_splitter.setSizes(
            [
                250,
                900,
            ],
        )

        layout.addWidget(
            main_splitter,
        )

        layout.addWidget(
            self.status_label,
        )

    def set_document_service(
        self,
        service: WorkspaceDocumentService,
    ) -> None:
        """Attach document service."""

        self._document_service = service

        self.refresh()

    def set_collection_service(
        self,
        service: CollectionService,
    ) -> None:
        """Attach collection service."""

        self._collection_service = service

        self.refresh_collections()

    def refresh_collections(
        self,
    ) -> None:
        """Reload collections."""

        if self._collection_service is None:

            self.collections.set_collections(
                [],
            )

            return

        self.collections.set_collections(
            self._collection_service.list_collections(),
        )

    def set_bookmark_service(
        self,
        service: BookmarkService,
    ) -> None:

        self._bookmark_service = service

        self.details.set_bookmark_service(
            service,
        )

    def set_note_service(
        self,
        service: NoteService,
    ) -> None:

        self._note_service = service

        self.details.set_note_service(
            service,
        )

    def clear_document_service(
        self,
    ) -> None:
        """Clear document services."""

        self._document_service = None

        self._bookmark_service = None

        self._note_service = None

        self.table.clear()

        self.details.clear()

        self.collections.set_collections(
            [],
        )

        self.status_label.setText(
            "No workspace open",
        )

    @property
    def document_service(
        self,
    ) -> WorkspaceDocumentService | None:
        """Return current document service."""

        return self._document_service

    @property
    def documents_directory(
        self,
    ) -> Path | None:
        """Return workspace documents directory."""

        if self._document_service is None:
            return None

        return self._document_service.documents_dir

    def refresh(
        self,
    ) -> None:
        """Reload documents."""

        if self._document_service is None:

            self.table.clear()

            self.details.clear()

            self.refresh_collections()

            self.status_label.setText(
                "No workspace open",
            )

            return

        documents = (
            self._document_service.list_documents()
        )

        self.table.set_documents(
            documents,
        )

        self.refresh_collections()

        self.status_label.setText(
            f"{len(documents)} document(s)",
        )

    def refresh_documents(
        self,
    ) -> None:
        """
        Refresh after document imports.
        """

        self.refresh()

    def _on_collection_selected(
        self,
        collection,
    ) -> None:
        """Filter documents by collection."""

        if collection is None:
            self.refresh()
            return

        if (
            self._collection_service is None
            or self._document_service is None
        ):
            return

        document_ids = (
            self._collection_service.list_documents(
                collection.id,
            )
        )

        documents = (
            self._document_service.list_documents()
        )

        filtered_documents = [
            document
            for document in documents
            if document.id in document_ids
        ]

        self.table.set_documents(
            filtered_documents,
        )

        self.details.clear()

        self.status_label.setText(
            f"{len(filtered_documents)} document(s)",
        )

    def add_selected_document_to_collection(
        self,
    ) -> None:
        """Add selected document to collection."""

        if (
            self._collection_service is None
            or self.selected_document() is None
        ):
            return

        collections = (
            self._collection_service.list_collections()
        )

        if not collections:
            return

        names = [
            collection.name
            for collection in collections
        ]

        name, ok = QInputDialog.getItem(
            self,
            "Add to Collection",
            "Collection:",
            names,
            0,
            False,
        )

        if not ok:
            return

        collection = next(
            (
                item
                for item in collections
                if item.name == name
            ),
            None,
        )

        if collection is None:
            return

        self._collection_service.add_document(
            collection.id,
            self.selected_document().id,
        )

        self.status_label.setText(
            f"Added to {collection.name}",
        )

    def _on_document_selected(
        self,
    ) -> None:
        """Display selected document."""

        document = self.selected_document()

        if document is None:

            self.details.clear()

            return

        self.details.show_document(
            document,
        )

    def selected_document(
        self,
    ) -> Document | None:

        return self.table.selected_document()

    def import_document(
        self,
        source: Path,
    ) -> None:

        if self._document_service is None:
            return

        self._document_service.import_document(
            source,
        )

        self.refresh()

    def import_folder(
        self,
        folder: Path,
    ) -> None:

        if self._document_service is None:
            return

        self._document_service.import_folder(
            folder,
        )

        self.refresh()

    def delete_selected_document(
        self,
    ) -> None:

        if self._document_service is None:
            return

        document = self.selected_document()

        if document is None:
            return

        self._document_service.remove_document(
            document.path,
        )

        self.refresh()

    def clear(
        self,
    ) -> None:

        self.table.clear()

        self.details.clear()

        self.collections.set_collections(
            [],
        )

        self.status_label.setText(
            "No workspace open",
        )