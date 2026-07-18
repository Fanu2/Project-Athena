"""Dialog for creating a new Athena workspace."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)


class NewWorkspaceDialog(QDialog):
    """Dialog used to create a new workspace."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("New Workspace")
        self.setMinimumWidth(500)

        self.name_edit = QLineEdit()

        self.location_edit = QLineEdit()

        self.browse_button = QPushButton("Browse...")

        self.create_button = QPushButton("Create")
        self.cancel_button = QPushButton("Cancel")

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:

        form = QFormLayout()

        form.addRow("Workspace Name:", self.name_edit)

        location_layout = QHBoxLayout()
        location_layout.addWidget(self.location_edit)
        location_layout.addWidget(self.browse_button)

        form.addRow("Location:", location_layout)

        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self.create_button)
        buttons.addWidget(self.cancel_button)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addStretch()
        layout.addLayout(buttons)

    def _connect_signals(self) -> None:
        self.browse_button.clicked.connect(self._browse)
        self.create_button.clicked.connect(self._validate)
        self.cancel_button.clicked.connect(self.reject)

    def _browse(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Workspace Location",
        )

        if folder:
            self.location_edit.setText(folder)

    def _validate(self) -> None:

        if not self.name_edit.text().strip():
            QMessageBox.warning(
                self,
                "Missing Name",
                "Please enter a workspace name.",
            )
            return

        if not self.location_edit.text().strip():
            QMessageBox.warning(
                self,
                "Missing Location",
                "Please choose a location.",
            )
            return

        self.accept()

    @property
    def workspace_name(self) -> str:
        return self.name_edit.text().strip()

    @property
    def workspace_location(self) -> Path:
        return Path(self.location_edit.text())
