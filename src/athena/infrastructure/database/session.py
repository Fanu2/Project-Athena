"""
SQLAlchemy session factory.
"""

from __future__ import annotations

from sqlalchemy.orm import sessionmaker

from athena.infrastructure.database.engine import engine

SessionFactory = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)