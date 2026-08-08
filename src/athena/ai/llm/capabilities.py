"""
Model capability definitions.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ModelCapabilities:
    """Capabilities supported by an LLM model."""

    chat: bool = True
    streaming: bool = False
    tools: bool = False
    vision: bool = False
    embeddings: bool = False
    reasoning: bool = False
    reranking: bool = False
    local: bool = False
