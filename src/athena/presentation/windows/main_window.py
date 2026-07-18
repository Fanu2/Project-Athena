"""
Main application window.
"""

from pathlib import Path

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QStackedWidget,
    QStatusBar,
    QToolBar,
)

from athena.documents.service import DocumentService
from athena.presentation.actions.document_actions import (
    DocumentActions,
)
from athena.presentation.actions.workspace_actions import (
    WorkspaceActions,
)
from athena.presentation.dialogs.new_workspace_dialog import (
    NewWorkspaceDialog,
)
from athena.presentation.navigation.navigation_widget import (
    NavigationWidget,
)
from athena.presentation.pages.document_library_page import (
    DocumentLibraryPage,
)
from athena.presentation.pages.home_page import (
    HomePage,
)
from athena.workspace.exceptions import (
    WorkspaceError,
)
from athena.workspace.models import (
    Workspace,
)


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        """Initialize the main window."""
        super().__init__()

        self.setWindowTitle("Athena")
        self.resize(1400, 900)

        self.workspace_actions = WorkspaceActions()
        self.current_workspace: Workspace | None = None

        self.navigation: NavigationWidget
        self.home: HomePage
        self.status_bar: QStatusBar
        self.toolbar: QToolBar

        self._create_actions()
        self._create_menu()
        self._create_toolbar()
        self._create_ui()
        self._create_status_bar()

        self._update_action_states()
        self.show_home()
        self.documents: DocumentLibraryPage
        self.page_stack: QStackedWidget
        self.document_actions: DocumentActions

    def _create_actions(self) -> None:
        """Create application actions."""

        self.new_workspace_action = QAction(
            "New Workspace...",
            self,
        )
        self.new_workspace_action.triggered.connect(
            self._on_new_workspace,
        )

        self.open_workspace_action = QAction(
            "Open Workspace...",
            self,
        )
        self.open_workspace_action.triggered.connect(
            self._on_open_workspace,
        )

        self.close_workspace_action = QAction(
            "Close Workspace",
            self,
        )
        self.close_workspace_action.triggered.connect(
            self._on_close_workspace,
        )

        self.exit_action = QAction(
            "Exit",
            self,
        )
        self.exit_action.triggered.connect(self.close)

    def _create_menu(self) -> None:
        """Create the application menu."""

        file_menu = self.menuBar().addMenu("&File")

        file_menu.addAction(self.new_workspace_action)
        file_menu.addAction(self.open_workspace_action)
        file_menu.addAction(self.close_workspace_action)

        file_menu.addSeparator()

        file_menu.addAction(self.exit_action)

    def _create_toolbar(self) -> None:
        """Create the main toolbar."""

        self.toolbar = QToolBar("Main")
        self.toolbar.setMovable(False)

        self.toolbar.addAction(self.new_workspace_action)
        self.toolbar.addAction(self.open_workspace_action)
        self.toolbar.addAction(self.close_workspace_action)

        self.addToolBar(self.toolbar)

    def _create_ui(self) -> None:
        """Create the central user interface."""

        splitter = QSplitter()

        self.navigation = NavigationWidget()

        self.page_stack = QStackedWidget()

        self.home = HomePage()

        self.documents = DocumentLibraryPage()

        self.document_actions = DocumentActions(
            self.documents,
        )

        self.page_stack.addWidget(self.home)
        self.page_stack.addWidget(self.documents)

        splitter.addWidget(self.navigation)
        splitter.addWidget(self.page_stack)

        splitter.setStretchFactor(1, 1)

        self.setCentralWidget(splitter)

        self.navigation.home_selected.connect(
            self.show_home,
        )

        self.navigation.documents_selected.connect(
            self.show_documents,
        )

    def show_home(self) -> None:
        """Display the Home page."""

        self.page_stack.setCurrentWidget(
            self.home,
        )

    def show_documents(self) -> None:
        """Display the Document Library page."""

        self.page_stack.setCurrentWidget(
            self.documents,
        )

    def _create_status_bar(self) -> None:
        """Create the application status bar."""

        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Ready")

        self.setStatusBar(self.status_bar)

    def _update_action_states(self) -> None:
        """Update enabled state of actions."""

        workspace_open = self.current_workspace is not None

        self.close_workspace_action.setEnabled(workspace_open)

    def _set_current_workspace(
        self,
        workspace: Workspace,
    ) -> None:
        """Set the active workspace."""

        self.current_workspace = workspace

        self.home.set_workspace(workspace)

        document_service = DocumentService(
            workspace.path / "documents",
        )

        self.documents.set_document_service(
            document_service,
        )

        self.status_bar.showMessage(f"Workspace: {workspace.name}")

        self.setWindowTitle(f"Athena — {workspace.name}")

        self._update_action_states()

    def _clear_current_workspace(self) -> None:
        """Clear the active workspace."""

        self.current_workspace = None

        self.home.clear_workspace()

        self.documents.clear_document_service()

        self.status_bar.showMessage("Ready")

        self.setWindowTitle("Athena")

        self._update_action_states()

    def _on_new_workspace(self) -> None:
        """Handle File → New Workspace."""

        dialog = NewWorkspaceDialog(self)

        if dialog.exec():
            try:
                workspace = self.workspace_actions.create_workspace(
                    dialog.workspace_location,
                    dialog.workspace_name,
                )

                self._set_current_workspace(workspace)

            except WorkspaceError as exc:
                QMessageBox.critical(
                    self,
                    "Workspace Error",
                    str(exc),
                )

    def _on_open_workspace(self) -> None:
        """Handle File → Open Workspace."""

        folder = QFileDialog.getExistingDirectory(
            self,
            "Open Workspace",
        )

        if not folder:
            return

        try:
            workspace = self.workspace_actions.open_workspace(
                Path(folder),
            )

            self._set_current_workspace(workspace)

        except WorkspaceError as exc:
            QMessageBox.critical(
                self,
                "Workspace Error",
                str(exc),
            )

    def _on_close_workspace(self) -> None:
        """Handle File → Close Workspace."""

        if self.current_workspace is None:
            QMessageBox.information(
                self,
                "No Workspace",
                "No workspace is currently open.",
            )
            return

        self._clear_current_workspace()
