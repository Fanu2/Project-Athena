"""
Model compatibility validator.
"""

from __future__ import annotations

from athena.ai.llm.metadata import ProviderMetadata
from athena.ai.llm.model_info import ModelInfo


class ModelValidator:
    """Validate model capability compatibility."""

    def validate_capability(
        self,
        model: ModelInfo,
        metadata: ProviderMetadata,
        capability: str,
    ) -> bool:
        """Return whether model supports capability."""

        if capability == "chat":
            return metadata.supports_chat

        if capability == "streaming":
            return metadata.supports_streaming

        if capability == "tools":
            return metadata.supports_tools

        if capability == "vision":
            return metadata.supports_vision

        raise ValueError(
            f"Unknown capability: {capability}"
        )
