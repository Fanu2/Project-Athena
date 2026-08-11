"""
AI Control Center page.

Displays Athena AI runtime information,
provider registry, provider health status,
active runtime information,
and evidence intelligence.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)

from athena.ai.providers.provider_health_group import (
    ProviderHealthGroup,
)

from athena.core.application_context import (
    ApplicationContext,
)

from athena.presentation.ai.evidence_widget import (
    EvidenceWidget,
)


class AIControlCenterPage(QWidget):
    """
    Manage Athena AI runtime.
    """

    def __init__(
        self,
        context: ApplicationContext,
        parent: QWidget | None = None,
    ) -> None:
        """
        Initialize AI Control Center.
        """

        super().__init__(parent)

        self._context = context

        self._layout = QVBoxLayout(
            self,
        )

        self._title = QLabel(
            "AI Control Center",
        )

        self._layout.addWidget(
            self._title,
        )

        self._registry_label = QLabel()

        self._layout.addWidget(
            self._registry_label,
        )

        self._providers_label = QLabel()

        self._layout.addWidget(
            self._providers_label,
        )

        self._models_label = QLabel()

        self._layout.addWidget(
            self._models_label,
        )

        self._runtime_label = QLabel()

        self._layout.addWidget(
            self._runtime_label,
        )

        #
        # Evidence Intelligence
        #

        self._evidence_widget = EvidenceWidget()

        self._layout.addWidget(
            self._evidence_widget,
        )

        self.refresh()


    def refresh(
        self,
    ) -> None:
        """
        Refresh AI runtime information.
        """

        self._refresh_provider_registry()

        self._refresh_provider_health()

        self._refresh_models()

        self._refresh_runtime()


    def clear_evidence(
        self,
    ) -> None:
        """
        Clear evidence intelligence display.
        """

        self._evidence_widget.clear()


    def set_evidence(
        self,
        evidence,
    ) -> None:
        """
        Display evidence intelligence.
        """

        self._evidence_widget.set_evidence(
            evidence,
        )


    def _refresh_provider_registry(
        self,
    ) -> None:
        """
        Display registered AI providers.
        """

        registry = (
            self._context.get_provider_registry()
        )

        providers = registry.providers()

        if not providers:
            self._registry_label.setText(
                "Provider Registry\n\n"
                "No providers registered."
            )
            return

        lines = [
            "Provider Registry",
            "",
        ]

        for provider in providers:
            lines.extend(
                [
                    f"Provider: {provider.name}",
                    f"ID: {provider.provider_id}",
                    (
                        "Endpoint: "
                        f"{provider.endpoint or 'local'}"
                    ),
                    (
                        "Capabilities: "
                        + ", ".join(
                            sorted(
                                provider.capabilities
                            )
                        )
                    ),
                    "",
                ]
            )

        self._registry_label.setText(
            "\n".join(lines),
        )


    def _refresh_provider_health(
        self,
    ) -> None:
        """
        Display aggregated provider health.
        """

        health = (
            self._context.get_provider_health()
        )

        if not health:
            self._providers_label.setText(
                "AI Providers\n\n"
                "No provider information available."
            )
            return

        groups = (
            ProviderHealthGroup.from_health(
                health,
            )
        )

        lines = [
            "AI Providers",
            "",
        ]

        for provider in groups:

            lines.extend(
                [
                    f"Provider: {provider.provider_id}",
                    f"Status: {provider.status}",
                    "",
                    "Models:",
                ]
            )

            for model in provider.models:
                lines.append(
                    f"  • {model}"
                )

            lines.extend(
                [
                    "",
                    (
                        "Capabilities: "
                        + ", ".join(
                            sorted(
                                provider.capabilities
                            )
                        )
                    ),
                    "",
                ]
            )

        self._providers_label.setText(
            "\n".join(lines),
        )


    def _refresh_models(
        self,
    ) -> None:
        """
        Display installed models.
        """

        manager = self._context.model_manager

        if manager is None:
            self._models_label.setText(
                "Installed Models\n\n"
                "Model Manager unavailable.\n"
                "Open a workspace to initialize AI runtime."
            )
            return

        lines = [
            "Installed Models",
            "",
        ]

        for model in manager.models():

            capabilities = []

            if model.capabilities.chat:
                capabilities.append("chat")

            if model.capabilities.streaming:
                capabilities.append("streaming")

            if model.capabilities.tools:
                capabilities.append("tools")

            if model.capabilities.vision:
                capabilities.append("vision")

            if model.capabilities.embeddings:
                capabilities.append("embedding")

            if model.capabilities.reasoning:
                capabilities.append("reasoning")

            if model.capabilities.reranking:
                capabilities.append("reranking")

            lines.extend(
                [
                    model.name,
                    f"Provider: {model.provider}",
                    (
                        "Capabilities: "
                        + (
                            ", ".join(capabilities)
                            if capabilities
                            else "none"
                        )
                    ),
                    "",
                ]
            )

        self._models_label.setText(
            "\n".join(lines),
        )


    def _refresh_runtime(
        self,
    ) -> None:
        """
        Display current AI runtime information.
        """

        manager = self._context.model_manager

        if manager is None:
            self._runtime_label.setText(
                "Runtime Information\n\n"
                "AI runtime unavailable.\n"
                "Open a workspace first."
            )
            return

        try:
            model = manager.active_model()

        except Exception as exc:
            self._runtime_label.setText(
                (
                    "Runtime Information\n\n"
                    "Runtime model unavailable.\n"
                    f"Reason: {exc}"
                )
            )
            return

        capabilities = []

        if model.capabilities.chat:
            capabilities.append("Chat")

        if model.capabilities.reasoning:
            capabilities.append("Reasoning")

        if model.capabilities.tools:
            capabilities.append("Tools")

        if model.capabilities.vision:
            capabilities.append("Vision")

        if model.capabilities.embeddings:
            capabilities.append("Embeddings")

        if model.capabilities.streaming:
            capabilities.append("Streaming")

        self._runtime_label.setText(
            (
                "Runtime Information\n\n"
                f"Model: {model.name}\n"
                f"Provider: {model.provider}\n"
                f"Context: {model.context_window}\n"
                "Capabilities: "
                f"{', '.join(capabilities) if capabilities else 'None'}"
            )
        )
