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

        capabilities = model.capabilities

        if capability == "chat":
            return capabilities.chat

        if capability == "streaming":
            return capabilities.streaming

        if capability == "tools":
            return capabilities.tools

        if capability == "vision":
            return capabilities.vision

        if capability == "embedding":
            return capabilities.embeddings

        if capability == "reasoning":
            return capabilities.reasoning

        if capability == "reranking":
            return capabilities.reranking

        raise ValueError(
            f"Unknown capability: {capability}"
        )