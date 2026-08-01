"""
Citation intelligence widget.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QLabel,
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
    """Display resolved citation intelligence and validation."""

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        """Initialize citation widget."""

        super().__init__(parent)

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

        self.details = QPlainTextEdit()

        self.details.setReadOnly(
            True,
        )

        self.details.setPlaceholderText(
            "Citation explanation...",
        )

        layout = QVBoxLayout(
            self,
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
            self.details,
        )

        self.clear()

    def set_citation(
        self,
        citation: ResolvedCitation,
        validation: CitationValidation | None = None,
    ) -> None:
        """
        Display citation intelligence.

        Includes:
        - source information
        - ranking explanation
        - validation result
        """

        self.source_label.setText(
            f"Source: {citation.document_name}",
        )

        self.page_label.setText(
            f"Page: {citation.page}",
        )

        self.score_label.setText(
            f"Score: {citation.score:.3f}",
        )

        explanation = (
            "Why selected:\n\n"
            + "\n".join(
                citation.reasons,
            )
            + "\n\nSupporting passage:\n\n"
            + citation.snippet
        )

        if validation is not None:

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

            explanation += (
                "\n\nValidation reasons:\n\n"
                + "\n".join(
                    validation.reasons,
                )
            )

        else:

            self.validation_label.setText(
                "Validation: unavailable",
            )

        self.details.setPlainText(
            explanation,
        )

    def clear(
        self,
    ) -> None:
        """Clear displayed citation."""

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