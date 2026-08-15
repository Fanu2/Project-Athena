"""
Athena collection domain model.

Represents a user-defined workspace collection.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Collection:
    """
    User-defined knowledge collection.
    """

    id: UUID = field(
        default_factory=uuid4,
    )

    name: str = ""

    description: str = ""

    created_at: datetime = field(
        default_factory=datetime.now,
    )

    updated_at: datetime = field(
        default_factory=datetime.now,
    )
