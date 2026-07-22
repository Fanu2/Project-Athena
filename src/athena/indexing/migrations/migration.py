"""
Base class for database migrations.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

import sqlite3


class Migration(ABC):
    """Base class for all database migrations."""

    version: int

    @abstractmethod
    def apply(
        self,
        connection: sqlite3.Connection,
    ) -> None:
        """Apply the migration."""