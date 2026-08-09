"""
Structured query intent model.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class QueryIntent:
    """
    Structured representation of a parsed user query.

    Used by retrieval planning and ranking selection.
    """

    original_query: str

    semantic_query: str

    #
    # Existing extraction fields
    #

    document_names: tuple[str, ...] = ()

    languages: tuple[str, ...] = ()

    file_types: tuple[str, ...] = ()

    collections: tuple[str, ...] = ()

    filters: dict[str, str] = field(
        default_factory=dict,
    )

    #
    # A19 Retrieval Intelligence
    #

    strategy: str = "hybrid"

    ranking_profile: str = "default"

    entities: tuple[str, ...] = ()

    confidence: float = 0.0
