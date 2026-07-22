"""
Intent Engine data models.

This module defines the core data structures used throughout the
Athena Intent Engine. It intentionally contains no business logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


class IntentType(Enum):
    """
    High-level user intent classifications.
    """

    UNKNOWN = auto()

    QUESTION = auto()

    SEARCH = auto()

    SUMMARIZE = auto()

    EXPLAIN = auto()

    COMPARE = auto()

    ANALYZE = auto()

    EXTRACT = auto()

    TRANSFORM = auto()

    CREATIVE = auto()


@dataclass(frozen=True, slots=True)
class MatchedIntent:
    """
    Represents a single keyword match for a detected intent.

    Attributes
    ----------
    intent
        Intent associated with the matched keyword.

    keyword
        The keyword that matched.

    occurrences
        Number of times the keyword appears in the normalized query.
    """

    intent: IntentType

    keyword: str

    occurrences: int = 1


@dataclass(frozen=True, slots=True)
class ConfidenceResult:
    """
    Result produced by the confidence calculator.
    """

    intent: IntentType

    confidence: float

    scores: dict[IntentType, int] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class IntentResult:
    """
    Result produced by the Intent Engine.

    Attributes
    ----------
    intent
        Detected user intent.

    confidence
        Confidence score between 0.0 and 1.0.

    matched_keywords
        Keywords contributing to the detected intent.

    modifiers
        Optional modifiers extracted from the query.

    normalized_query
        Normalized query used internally.
    """

    intent: IntentType

    confidence: float = 0.0

    matched_keywords: tuple[str, ...] = field(default_factory=tuple)

    modifiers: tuple[str, ...] = field(default_factory=tuple)

    normalized_query: str = ""