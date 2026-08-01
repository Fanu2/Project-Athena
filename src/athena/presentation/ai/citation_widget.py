"""
Citation intelligence widget.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QPushButton,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

from athena.domain.ai.citation_validation import (
    CitationValidation,
)

from athena.domain.ai.resolved_citation import (
    ResolvedCitation,
)


class CitationWidget(QWidget):
    """Display multiple citations with intelligence details."""

    document_requested = Signal(
        Path,
        int,
    )

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        """Initialize citation widget."""

        super().__init__(parent)

        self._citations: list[ResolvedCitation] = []

        self._validations: list[CitationValidation] = []

        self.citation_list = QListWidget()

        self.source_label = QLabel(
            "Source: -",
        )

        self.page_label = QLabel(
            "Page: -",
        )

        self.score_label = QLabel(
            "Score: -",
        )

        self.validation_label = QLabel(
            "Validation: -",
        )

        self.open_button = QPushButton(
            "Open Source Document",
        )

        self.details = QPlainTextEdit()

        self.details.setReadOnly(
            True,
        )

        layout = QVBoxLayout(
            self,
        )

        layout.addWidget(
            QLabel("Citations"),
        )

        layout.addWidget(
            self.citation_list,
        )

        layout.addWidget(
            self.source_label,
        )

        layout.addWidget(
            self.page_label,
        )

        layout.addWidget(
            self.score_label,
        )

        layout.addWidget(
            self.validation_label,
        )

        layout.addWidget(
            self.open_button,
        )

        layout.addWidget(
            self.details,
        )

        self.citation_list.currentRowChanged.connect(
            self._show_selected_citation,
        )

        self.open_button.clicked.connect(
            self._open_source,
        )

        self.clear()

    def set_citations(
        self,
        citations: list[ResolvedCitation],
        validations: list[CitationValidation] | None = None,
    ) -> None:
        """Display citation list."""

        self._citations = citations

        self._validations = (
            validations
            if validations is not None
            else []
        )

        self.citation_list.clear()

        for index, citation in enumerate(
            citations,
            start=1,
        ):
            self.citation_list.addItem(
                (
                    f"{index}. "
                    f"{citation.document_name} "
                    f"(p.{citation.page})"
                ),
            )

        if citations:
            self.citation_list.setCurrentRow(
                0,
            )
        else:
            self.clear()

    def _show_selected_citation(
        self,
        index: int,
    ) -> None:
        """Show selected citation details."""

        if index < 0:
            return

        if index >= len(
            self._citations,
        ):
            return

        citation = self._citations[index]

        validation = None

        if index < len(
            self._validations,
        ):
            validation = self._validations[index]

        self.source_label.setText(
            f"Source: {citation.document_name}",
        )

        self.page_label.setText(
            f"Page: {citation.page}",
        )

        self.score_label.setText(
            f"Score: {citation.score:.3f}",
        )

        if validation:

            status = (
                "VALID"
                if validation.supported
                else "NOT VERIFIED"
            )

            self.validation_label.setText(
                (
                    f"Validation: {status} "
                    f"({validation.confidence:.3f})"
                ),
            )

            validation_text = (
                "\n\nValidation reasons:\n\n"
                + "\n".join(
                    validation.reasons,
                )
            )

        else:

            self.validation_label.setText(
                "Validation: unavailable",
            )

            validation_text = ""

        explanation = (
            "Why selected:\n\n"
            + "\n".join(
                citation.reasons,
            )
            + "\n\nSupporting passage:\n\n"
            + citation.snippet
            + validation_text
        )

        self.details.setPlainText(
            explanation,
        )

    def _open_source(
        self,
    ) -> None:
        """Open selected citation document."""

        index = self.citation_list.currentRow()

        if index < 0:
            return

        if index >= len(
            self._citations,
        ):
            return

        citation = self._citations[index]

        if citation.document_path is None:
            return

        self.document_requested.emit(
            citation.document_path,
            citation.page,
        )

    def clear(
        self,
    ) -> None:
        """Clear citations."""

        self._citations.clear()

        self._validations.clear()

        self.citation_list.clear()

        self.source_label.setText(
            "Source: -",
        )

        self.page_label.setText(
            "Page: -",
        )

        self.score_label.setText(
            "Score: -",
        )

        self.validation_label.setText(
            "Validation: -",
        )

        self.details.clear()