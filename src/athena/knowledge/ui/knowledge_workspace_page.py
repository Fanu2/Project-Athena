"""
Knowledge Workspace page.

Displays workspace knowledge items,
selected knowledge details,
evidence, and citations.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)

from athena.knowledge.models.workspace_knowledge_item import (
    WorkspaceKnowledgeItem,
)

from athena.services.knowledge_workspace_service import (
    KnowledgeWorkspaceService,
)


class KnowledgeWorkspacePage(QWidget):
    """
    Displays Athena workspace knowledge.
    """

    def __init__(
        self,
        service: KnowledgeWorkspaceService | None = None,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self._service = service

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels(
            [
                "Title",
                "Type",
                "Confidence",
                "Source",
            ]
        )

        self.details = QLabel(
            "Select a knowledge item.",
        )

        self.details.setWordWrap(
            True,
        )

        self.table.itemSelectionChanged.connect(
            self._show_details,
        )

        layout = QHBoxLayout(
            self,
        )

        layout.addWidget(
            self.table,
        )

        layout.addWidget(
            self.details,
        )

    def set_service(
        self,
        service: KnowledgeWorkspaceService,
    ) -> None:
        """
        Set workspace knowledge service.
        """

        self._service = service

    def refresh(self) -> None:
        """
        Reload knowledge items.
        """

        if self._service is None:
            self.table.setRowCount(
                0,
            )
            return

        items = (
            self._service
            .list_workspace_items()
        )

        self.table.setRowCount(
            len(items),
        )

        for row, item in enumerate(items):

            values = [
                item.title or "-",
                item.object_type,
                f"{item.confidence:.2f}",
                item.source_reference or "-",
            ]

            for column, value in enumerate(values):

                self.table.setItem(
                    row,
                    column,
                    QTableWidgetItem(
                        value,
                    ),
                )

    def _show_details(self) -> None:
        """
        Display selected knowledge item details,
        evidence, and citations.
        """

        if self._service is None:
            return

        row = self.table.currentRow()

        if row < 0:
            return

        items = (
            self._service
            .list_workspace_items()
        )

        if row >= len(items):
            return

        item: WorkspaceKnowledgeItem = items[row]

        lines = [
            "Knowledge Details",
            "",
            f"Title: {item.title or '-'}",
            f"Type: {item.object_type}",
            f"Confidence: {item.confidence:.2f}",
            f"Source: {item.source_reference or '-'}",
            f"Provider: {item.provider or '-'}",
            f"Extraction: {item.extraction_method or '-'}",
            "",
            "Evidence",
            "",
        ]

        evidence_items = (
            self._service
            .get_evidence(
                item.object_id,
            )
        )

        if not evidence_items:
            lines.append(
                "No evidence available."
            )

        for evidence in evidence_items:

            lines.extend(
                [
                    (
                        "Source: "
                        f"{evidence.source_reference or '-'}"
                    ),
                    (
                        "Location: "
                        f"{evidence.location or '-'}"
                    ),
                    (
                        "Method: "
                        f"{evidence.extraction_method or '-'}"
                    ),
                    (
                        "Confidence: "
                        f"{evidence.confidence:.2f}"
                    ),
                    "",
                    "Citations",
                    "",
                ]
            )

            citations = (
                self._service
                .get_citations(
                    evidence.evidence_id,
                )
            )

            if not citations:
                lines.append(
                    "No citations available."
                )

            for citation in citations:

                lines.extend(
                    [
                        (
                            "Text: "
                            f"{citation.citation_text or '-'}"
                        ),
                        (
                            "Location: "
                            f"{citation.location or '-'}"
                        ),
                        (
                            "Confidence: "
                            f"{citation.confidence:.2f}"
                        ),
                        "",
                    ]
                )

        self.details.setText(
            "\n".join(lines),
        )