"""
Workspace AI settings model.
"""

from __future__ import annotations

from dataclasses import dataclass

from athena.core.defaults import DEFAULT_LLM_MODEL


@dataclass(slots=True)
class AISettings:
    """Workspace AI settings."""

    default_model: str = DEFAULT_LLM_MODEL