"""A20 workspace presentation page."""

from __future__ import annotations

from typing import Any

from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QVBoxLayout,
    QWidget,
)

from athena.presentation.workspace.provider import WorkspaceViewProvider


class WorkspacePage(QWidget):
    """Displays the A20 workspace hierarchy."""

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._provider: WorkspaceViewProvider | None = None
        self._workspace_id: str | None = None

        self.title_label = QLabel("Workspace")
        self.summary_label = QLabel()

        self.projects_list = QListWidget()
        self.collections_list = QListWidget()
        self.documents_list = QListWidget()
        self.notes_list = QListWidget()

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Create the page layout."""

        layout = QVBoxLayout(self)

        layout.addWidget(self.title_label)
        layout.addWidget(self.summary_label)

        layout.addWidget(QLabel("Projects"))
        layout.addWidget(self.projects_list)

        layout.addWidget(QLabel("Collections"))
        layout.addWidget(self.collections_list)

        layout.addWidget(QLabel("Documents"))
        layout.addWidget(self.documents_list)

        layout.addWidget(QLabel("Notes"))
        layout.addWidget(self.notes_list)

    def set_workspace_provider(
        self,
        provider: WorkspaceViewProvider,
        workspace_id: str,
    ) -> None:
        """Attach the workspace presentation provider."""

        self._provider = provider
        self._workspace_id = workspace_id
        self.refresh()

    def showEvent(
        self,
        event: QShowEvent,
    ) -> None:
        """Refresh workspace state whenever the page becomes visible."""

        self.refresh()

        super().showEvent(event)

    def refresh(self) -> None:
        """Reload the workspace presentation state."""

        self.projects_list.clear()
        self.collections_list.clear()
        self.documents_list.clear()
        self.notes_list.clear()

        if self._provider is None or self._workspace_id is None:
            return

        model: Any = self._provider.build(
            self._workspace_id,
        )

        if model.workspace is None:
            return

        self.title_label.setText(
            model.workspace.name,
        )

        self.summary_label.setText(
            f"Projects: {model.workspace.project_count}  |  "
            f"Documents: {model.workspace.document_count}  |  "
            f"Notes: {model.workspace.note_count}"
        )

        for project in model.projects:
            self.projects_list.addItem(project.name)

        for collection in model.collections:
            self.collections_list.addItem(collection.name)

        for document in model.documents:
            self.documents_list.addItem(document.filename)

        for note in model.notes:
            self.notes_list.addItem(note.title)

    def clear(self) -> None:
        """Clear the displayed workspace."""

        self.projects_list.clear()
        self.collections_list.clear()
        self.documents_list.clear()
        self.notes_list.clear()
        self.summary_label.clear()
