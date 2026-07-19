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

from athena.core.application_context import ApplicationContext
from athena.presentation.actions.document_actions import (
    DocumentActions,
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
from athena.presentation.search.search_workspace import (
    SearchWorkspace,
)
from athena.presentation.pages.bookmark_page import (
    BookmarkPage,
)
from athena.presentation.ai.ask_athena_page import (
    AskAthenaPage,
)
from athena.presentation.pages.indexed_documents_page import (
    IndexedDocumentsPage,
)
from athena.presentation.viewer import (
    DocumentViewerPage,
)


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(
        self,
        context: ApplicationContext,
    ) -> None:
        """Initialize the main window."""
        super().__init__()

        self.context = context
        self.workspace_actions = context.workspace_actions

        self.setWindowTitle("Athena")
        self.resize(1400, 900)

        self.current_workspace: Workspace | None = None

        self.navigation: NavigationWidget
        self.home: HomePage
        self.documents: DocumentLibraryPage
        self.indexed_documents: IndexedDocumentsPage
        self.search: SearchWorkspace
        self.ask_athena: AskAthenaPage
        self.page_stack: QStackedWidget
        self.status_bar: QStatusBar
        self.toolbar: QToolBar
        self.document_actions: DocumentActions
        self.viewer: DocumentViewerPage
        self.bookmarks = BookmarkPage()

        self._create_actions()
        self._create_menu()
        self._create_toolbar()
        self._create_ui()
        self._create_status_bar()

        self._update_action_states()
        self.show_home()

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
        self.indexed_documents = IndexedDocumentsPage(  # NEW
            self.context.indexed_document_service,  # NEW
        )  # NEW
        self.search = SearchWorkspace()
        self.bookmarks = BookmarkPage()
        self.ask_athena = AskAthenaPage()

        self.viewer = DocumentViewerPage()
        self.viewer.set_viewer_service(
            self.context.document_viewer_service,
        )

        self.document_actions = DocumentActions(
            self.documents,
        )

        self.page_stack.addWidget(
            self.home,
        )
        self.page_stack.addWidget(
            self.indexed_documents,
        )

        self.page_stack.addWidget(
            self.documents,
        )

        self.page_stack.addWidget(
            self.search,
        )

        self.page_stack.addWidget(
            self.bookmarks,
        )

        self.page_stack.addWidget(
            self.ask_athena,
        )

        self.page_stack.addWidget(
            self.viewer,
        )

        splitter.addWidget(
            self.navigation,
        )

        splitter.addWidget(
            self.page_stack,
        )

        splitter.setStretchFactor(
            1,
            1,
        )

        self.setCentralWidget(
            splitter,
        )

        self.navigation.home_selected.connect(
            self.show_home,
        )

        self.navigation.documents_selected.connect(
            self.show_documents,
        )

        self.navigation.indexed_documents_selected.connect(  # NEW
            self.show_indexed_documents,  # NEW
        )  # NEW

        self.navigation.search_selected.connect(
            self.show_search,
        )

        self.navigation.bookmarks_selected.connect(
            self.show_bookmarks,
        )

        self.navigation.ai_selected.connect(
            self.show_ai,
        )

        self.documents.table.document_activated.connect(
            self._open_document_viewer,
        )

        self.ask_athena.document_requested.connect(
            self._open_ai_source,
        )

    def show_home(self) -> None:
        """Display the Home page."""

        self.page_stack.setCurrentWidget(
            self.home,
        )

    def show_indexed_documents(self) -> None:
        """Display the Indexed Documents page."""

        self.page_stack.setCurrentWidget(
            self.indexed_documents,
        )

    def show_documents(self) -> None:
        """Display the Document Library page."""

        self.page_stack.setCurrentWidget(
            self.documents,
        )

    def show_bookmarks(self) -> None:
        """Display the bookmarks page."""

        self.page_stack.setCurrentWidget(
            self.bookmarks,
        )

    def show_search(self) -> None:
        """Display the Search page."""

        self.page_stack.setCurrentWidget(
            self.search,
        )

    def show_ai(self) -> None:
        """Show Ask Athena page."""

        self.page_stack.setCurrentWidget(
            self.ask_athena,
        )

    def _create_status_bar(self) -> None:
        """Create the application status bar."""

        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Ready")

        self.setStatusBar(self.status_bar)

    def _update_action_states(self) -> None:
        """Update enabled state of actions."""

        workspace_open = self.current_workspace is not None

        self.close_workspace_action.setEnabled(
            workspace_open,
        )

    def _set_current_workspace(
        self,
        workspace: Workspace,
    ) -> None:
        """Set the active workspace."""

        self.current_workspace = workspace

        self.home.set_workspace(
            workspace,
        )

        self.context.open_workspace(
            workspace.path,
        )

        document_service = self.context.document_service

        if document_service is not None:
            self.documents.set_document_service(
                document_service,
            )

            self.search.set_document_service(
                document_service.document_service,
            )

        # NEW: Connect Indexed Documents page to the newly created service
        indexed_document_service = self.context.indexed_document_service

        if indexed_document_service is not None:
            self.indexed_documents.set_document_service(
                indexed_document_service,
            )

        search_service = self.context.search_service

        if search_service is not None:
            self.search.set_search_service(
                search_service,
            )

        bookmark_service = self.context.bookmark_service

        if bookmark_service is not None:
            self.bookmarks.set_bookmark_service(
                bookmark_service,
            )

        rag_service = self.context.rag_service

        if rag_service is not None:
            self.ask_athena.set_rag_service(
                rag_service,
            )

        note_service = self.context.note_service

        if note_service is not None:
            self.documents.set_note_service(
                note_service,
            )

        self.status_bar.showMessage(
            f"Workspace: {workspace.name}",
        )

        self.setWindowTitle(
            f"Athena — {workspace.name}",
        )

        self._update_action_states()

    def _clear_current_workspace(self) -> None:
        """Clear the active workspace."""

        self.current_workspace = None

        self.home.clear_workspace()

        self.context.close_workspace()

        self.documents.clear_document_service()

        self.search.clear_search_service()

        self.bookmarks.clear()

        self.ask_athena.clear_rag_service()

        self.status_bar.showMessage(
            "Ready",
        )

        self.setWindowTitle(
            "Athena",
        )

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

                self._set_current_workspace(
                    workspace,
                )

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

            self._set_current_workspace(
                workspace,
            )

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

    def _open_document_viewer(
        self,
        path: Path,
    ) -> None:
        """Open a document in the viewer."""

        self.viewer.open_document(
            path,
            page=None,
        )

        self.page_stack.setCurrentWidget(
            self.viewer,
        )

    def _open_ai_source(
        self,
        path: Path,
        page: int,
    ) -> None:
        """Open a cited source from Ask Athena."""

        self.viewer.open_document(
            path,
            page=page,
        )

        self.page_stack.setCurrentWidget(
            self.viewer,
        )
