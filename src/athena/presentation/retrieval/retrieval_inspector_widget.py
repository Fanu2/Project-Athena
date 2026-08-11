"""
Retrieval Inspector.

Displays the retrieval results used to generate
an Athena answer.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QVBoxLayout,
    QWidget,
)

from athena.domain.ai.retrieval_result import RetrievalResult


class RetrievalInspectorWidget(QWidget):
    """
    Displays retrieved results.
    """

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._title = QLabel(
            "Retrieved Evidence",
        )

        self._results = QListWidget()

        layout = QVBoxLayout(self)

        layout.addWidget(
            self._title,
        )

        layout.addWidget(
            self._results,
        )

    def clear(self) -> None:
        """Clear displayed retrieval results."""

        self._results.clear()

    def set_results(
        self,
        results: list[RetrievalResult],
    ) -> None:
        """
        Populate the inspector with retrieval results.
        """

        self._results.clear()

        for result in results:
            preview = result.text.strip()

            if len(preview) > 250:
                preview = preview[:250] + "..."

            self._results.addItem(
                (
                    f"{result.document_name}\n"
                    f"Score : {result.score:.3f}\n"
                    f"Page  : {result.page}\n\n"
                    f"{preview}"
                )
            )