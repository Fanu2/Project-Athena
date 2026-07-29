"""
LM Studio provider.
"""

from __future__ import annotations

from athena.ai.llm.provider import LLMProvider
from athena.ai.llm.providers.openai_compatible import (
    OpenAICompatibleProvider,
)
from athena.settings import LLMSettings


class LMStudioProvider(OpenAICompatibleProvider):
    """LLM provider for LM Studio."""

    def __init__(
        self,
        settings: LLMSettings | None = None,
    ) -> None:
        super().__init__(
            settings
            if settings is not None
            else LLMSettings(
                provider="lmstudio",
                base_url="http://localhost:1234",
            )
        )

    @property
    def provider_name(self) -> str:
        return "lmstudio"
