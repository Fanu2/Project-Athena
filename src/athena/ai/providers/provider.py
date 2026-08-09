"""
AI provider domain model.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Provider:
    """
    Represents an AI runtime provider.

    Examples:
    - Ollama
    - llama.cpp
    - OpenAI-compatible API
    """

    provider_id: str

    name: str

    endpoint: str | None = None

    models: list[str] = field(
        default_factory=list,
    )

    capabilities: set[str] = field(
        default_factory=set,
    )

    model_capabilities: dict[str, set[str]] = field(
        default_factory=dict,
    )

    enabled: bool = True

    def capabilities_for_model(
        self,
        model_name: str,
    ) -> set[str]:
        """
        Return capabilities for a specific model.

        Falls back to provider-level capabilities
        when no model-specific mapping exists.
        """

        return self.model_capabilities.get(
            model_name,
            self.capabilities,
        )