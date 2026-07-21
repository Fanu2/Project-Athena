"""
Database initialization tests.
"""

from __future__ import annotations

from athena.infrastructure.database import initialize_database


def test_database_initialization() -> None:
    """Database should initialize without raising exceptions."""
    initialize_database()
