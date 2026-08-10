"""
Citation intelligence widget.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QGroupBox,
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
    """
    Display citation intelligence details.
    """

    document_requested = Signal(
        Path,
        int,
    )


    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        """
        Initialize citation widget.
        """

        super().__init__(
            parent,
        )

        self._citations: list[ResolvedCitation] = []

        self._validations: list[CitationValidation] = []


        #
        # Citation list
        #

        self.citation_list = QListWidget()

        self.citation_list.setAlternatingRowColors(
            True,
        )


        #
        # Intelligence summary
        #

        self.source_label = QLabel(
            "📄 Source: -",
        )

        self.page_label = QLabel(
            "Page: -",
        )

        self.score_label = QLabel(
            "Confidence: -",
        )

        self.validation_label = QLabel(
            "Validation: -",
        )


        #
        # Actions
        #

        self.open_button = QPushButton(
            "Open Source Document",
        )


        #
        # Evidence details
        #

        self.details = QPlainTextEdit()

        self.details.setReadOnly(
            True,
        )

        self.details.setLineWrapMode(
            QPlainTextEdit.LineWrapMode.WidgetWidth,
        )

        self.details.setPlaceholderText(
            "Citation evidence will appear here...",
        )


        #
        # Layout
        #

        citations_box = QGroupBox(
            "Citations",
        )

        citations_layout = QVBoxLayout(
            citations_box,
        )

        citations_layout.addWidget(
            self.citation_list,
        )


        intelligence_box = QGroupBox(
            "Citation Intelligence",
        )

        intelligence_layout = QVBoxLayout(
            intelligence_box,
        )

        intelligence_layout.addWidget(
            self.source_label,
        )

        intelligence_layout.addWidget(
            self.page_label,
        )

        intelligence_layout.addWidget(
            self.score_label,
        )

        intelligence_layout.addWidget(
            self.validation_label,
        )

        intelligence_layout.addWidget(
            self.open_button,
        )

        intelligence_layout.addWidget(
            self.details,
        )


        layout = QVBoxLayout(
            self,
        )

        layout.addWidget(
            citations_box,
        )

        layout.addWidget(
            intelligence_box,
        )


        #
        # Signals
        #

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
        """
        Display citation list.
        """

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
                    f"📄 {citation.document_name} "
                    f"(page {citation.page})"
                ),
            )

            item = self.citation_list.item(
                self.citation_list.count() - 1,
            )

            item.setToolTip(
                (
                    "Citation source\n"
                    f"Document: {citation.document_name}\n"
                    f"Page: {citation.page}\n"
                    f"Confidence: {citation.score:.1%}"
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
        """
        Display selected citation intelligence.
        """

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

            validation = (
                self._validations[index]
            )


        #
        # Summary
        #

        self.source_label.setText(
            (
                f"📄 Source: "
                f"{citation.document_name}"
            ),
        )

        self.page_label.setText(
            (
                f"Page: {citation.page}"
            ),
        )

        self.score_label.setText(
            (
                f"Confidence: "
                f"{citation.score:.1%}"
            ),
        )


        #
        # Validation
        #

        if validation:

            if validation.supported:

                status = "✓ VALID"

            else:

                status = "⚠ NOT VERIFIED"


            self.validation_label.setText(
                (
                    f"Validation: "
                    f"{status} "
                    f"({validation.confidence:.1%})"
                ),
            )


            validation_text = (
                "\n\n"
                "Validation reasons:\n\n"
                +
                "\n".join(
                    validation.reasons,
                )
            )

        else:

            self.validation_label.setText(
                "Validation: unavailable",
            )

            validation_text = ""


        #
        # Evidence intelligence
        #

        explanation = (
            "📊 Evidence Intelligence\n\n"
            f"Confidence: {citation.score:.1%}\n\n"
            "Why Athena selected this source:\n\n"
            +
            "\n".join(
                f"• {reason}"
                for reason in citation.reasons
            )
            +
            "\n\n"
            "Supporting passage:\n\n"
            +
            citation.snippet
            +
            validation_text
        )


        self.details.setPlainText(
            explanation,
        )


        self.open_button.setEnabled(
            citation.document_path is not None,
        )



    def _open_source(
        self,
    ) -> None:
        """
        Open selected citation document.
        """

        index = (
            self.citation_list.currentRow()
        )

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
        """
        Clear citations.
        """

        self._citations.clear()

        self._validations.clear()

        self.citation_list.clear()


        self.source_label.setText(
            "📄 Source: -",
        )

        self.page_label.setText(
            "Page: -",
        )

        self.score_label.setText(
            "Confidence: -",
        )

        self.validation_label.setText(
            "Validation: -",
        )


        self.open_button.setEnabled(
            False,
        )


        self.details.clear()