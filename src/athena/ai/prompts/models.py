"""
Prompt models.
"""

from __future__ import annotations

from dataclasses import dataclass

from athena.ai.citations import Citation
from athena.ai.retrieval.models import SemanticResult


@dataclass(slots=True, frozen=True)
class PromptRequest:
    """Information required to build an AI prompt."""

    question: str

    results: list[SemanticResult]

    citations: list[Citation]


@dataclass(slots=True, frozen=True)
class Prompt:
    """Final prompt ready for an LLM."""

    system: str

    user: str
