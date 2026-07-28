from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class QueryIntent:
    """
    Structured representation of a parsed user query.
    """

    original_query: str
    semantic_query: str

    document_names: tuple[str, ...] = ()
    languages: tuple[str, ...] = ()
    file_types: tuple[str, ...] = ()
    collections: tuple[str, ...] = ()

    filters: dict[str, str] = field(default_factory=dict)

