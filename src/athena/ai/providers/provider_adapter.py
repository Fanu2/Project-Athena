"""
Adapter between LLM providers and AI runtime providers.
"""

from __future__ import annotations

from athena.ai.llm.provider import LLMProvider
from athena.ai.providers.provider import Provider


class ProviderAdapter:
    """Convert LLMProvider into runtime Provider."""

    @staticmethod
    def from_llm_provider(
        llm_provider: LLMProvider,
    ) -> Provider:
        """Create runtime provider from LLM provider."""

        metadata = llm_provider.metadata

        capabilities = {
            name
            for name, enabled in (
                llm_provider.capabilities().items()
            )
            if enabled
        }

        models = []

        try:
            models = llm_provider.list_models()

        except Exception:
            models = []

        return Provider(
            provider_id=(
                llm_provider.provider_name
            ),
            name=metadata.display_name,
            models=models,
            capabilities=capabilities,
            enabled=(
                llm_provider.health()
            ),
        )
