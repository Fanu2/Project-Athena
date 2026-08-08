"""
Model profile definitions.

Maps Athena capabilities to preferred models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ModelProfile:
    """Defines a model assignment profile."""

    name: str
    capability: str
    model_name: str
    provider: str = "ollama"