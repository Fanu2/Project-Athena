"""
Database initialization utilities.
"""

from __future__ import annotations

# Import models so SQLAlchemy registers them.
from athena.infrastructure.database.models.document_model import (
    DocumentModel,  # noqa: F401
)
from athena.infrastructure.database.models.document_version_model import (
    DocumentVersionModel,  # noqa: F401
)

from athena.infrastructure.database.base import Base
from athena.infrastructure.database.engine import engine


def initialize_database() -> None:
    """Create all database tables."""

    Base.metadata.create_all(bind=engine)
