"""
Assistant workspace widget.

Composes session, memory,
conversation, and plan views.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QWidget,
)

from athena.application.assistant.workspace_service import (
    AssistantWorkspaceService,
)

from athena.presentation.ai.conversation_widget import (
    ConversationWidget,
)

from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)

from .assistant_memory import (
    AssistantMemoryWidget,
)

from .assistant_plan import (
    AssistantPlanWidget,
)

from .assistant_session import (
    AssistantSessionWidget,
)


class AssistantWorkspaceWidget(QFrame):
    """
    Workspace-level assistant container.
    """

    def __init__(
        self,
        service: AssistantWorkspaceService,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(
            parent,
        )

        self._service = service

        self.setFrameShape(
            QFrame.Shape.StyledPanel,
        )

        self.session_widget = (
            AssistantSessionWidget(
                self,
            )
        )

        self.memory_widget = (
            AssistantMemoryWidget(
                self,
            )
        )

        self.conversation_widget = (
            ConversationWidget(
                self,
            )
        )

        self.plan_widget = (
            AssistantPlanWidget(
                self,
            )
        )

        self._setup_ui()


    def _setup_ui(
        self,
    ) -> None:
        """
        Create assistant workspace layout.
        """

        layout = QVBoxLayout(
            self,
        )

        layout.setSpacing(
            8,
        )

        layout.addWidget(
            self.session_widget,
        )

        layout.addWidget(
            self.memory_widget,
        )

        layout.addWidget(
            self.conversation_widget,
        )

        layout.addWidget(
            self.plan_widget,
        )


    def create_plan(
        self,
        query: str,
        workspace: WorkspaceIntelligenceSnapshot,
    ):
        """
        Create and display assistant plan.
        """

        plan = (
            self._service.create_plan(
                query,
                workspace,
            )
        )

        self.plan_widget.set_plan(
            plan,
        )

        return plan
