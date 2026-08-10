"""
Athena workspace domain models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from uuid import UUID, uuid4


@dataclass(slots=True)
class Workspace:
    """
    Represents an Athena intelligent workspace.
    """

    name: str

    path: Path

    version: str

    created: datetime

    modified: datetime

    workspace_id: UUID = field(
        default_factory=uuid4,
    )

    description: str = ""

    metadata: dict[str, str] = field(
        default_factory=dict,
    )
