"""
Conversation widget.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QAbstractItemView,
    QListView,
    QVBoxLayout,
    QWidget,
)

from athena.presentation.ai.conversation_model import (
    ConversationModel,
)
from athena.presentation.ai.conversation_delegate import (
    ConversationDelegate,
)


class ConversationWidget(QWidget):
    """Widget displaying an Athena conversation."""

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        """Initialize the conversation widget."""
        super().__init__(parent)

        self._model: ConversationModel | None = None

        self.list_view = QListView()

        self._delegate = ConversationDelegate(
            self.list_view,
        )

        self.list_view.setItemDelegate(
            self._delegate,
        )

        self.list_view.setWordWrap(
            True,
        )

        self.list_view.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection,
        )

        self.list_view.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectItems,
        )

        self.list_view.setUniformItemSizes(
            False,
        )

        self.list_view.setAlternatingRowColors(
            True,
        )

        layout = QVBoxLayout(
            self,
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.addWidget(
            self.list_view,
        )

    def set_model(
        self,
        model: ConversationModel,
    ) -> None:
        """Attach a conversation model."""

        self._model = model

        self.list_view.setModel(
            model,
        )

    def refresh(
        self,
    ) -> None:
        """Refresh the displayed conversation."""

        if self._model is None:
            return

        self._model.refresh()

        self.list_view.scrollToBottom()

    def model(
        self,
    ) -> ConversationModel | None:
        """Return the attached conversation model."""

        return self._model
