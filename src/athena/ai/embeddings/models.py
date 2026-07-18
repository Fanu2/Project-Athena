"""
Embedding models.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class EmbeddingRecord:
    """Stored vector embedding."""

    chunk_id: str
    model_name: str
    vector: list[float]
    created: datetime
