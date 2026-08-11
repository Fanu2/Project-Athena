"""
Evidence Intelligence widget.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QLabel,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)


class EvidenceWidget(QWidget):
    """
    Displays evidence ranking intelligence.
    """

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self.title = QLabel(
            "Evidence Intelligence"
        )

        self.details = QPlainTextEdit()

        self.details.setReadOnly(
            True,
        )

        layout = QVBoxLayout(
            self,
        )

        layout.addWidget(
            self.title,
        )

        layout.addWidget(
            self.details,
        )


    def clear(self) -> None:
        self.details.clear()


    def set_evidence(
        self,
        evidence,
    ) -> None:

        if evidence is None:
            self.clear()
            return

        reasons = "\n".join(
            evidence.ranking_reasons,
        )

        text = (
            f"Confidence: "
            f"{evidence.final_score:.1%}\n\n"
            f"Score: "
            f"{evidence.final_score:.3f}\n\n"
            f"Why selected:\n"
            f"{reasons}"
        )

        self.details.setPlainText(
            text,
        )
