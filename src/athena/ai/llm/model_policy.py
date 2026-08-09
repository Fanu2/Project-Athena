"""
Model routing policy definitions.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ModelPolicy:
    """Defines model selection preferences."""

    name: str

    prefer_local: bool = True

    require_reasoning: bool = False

    require_vision: bool = False

    require_embeddings: bool = False

    latency_priority: bool = False

    quality_priority: bool = True