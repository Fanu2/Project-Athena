"""
Shared SQLAlchemy test fixtures.
"""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from athena.infrastructure.database.base import Base

# Register all SQLAlchemy models


@pytest.fixture
def test_session(tmp_path):
    """Provide an isolated SQLAlchemy session."""

    database = tmp_path / "athena_test.db"

    engine = create_engine(
        f"sqlite:///{database}",
        future=True,
    )

    Base.metadata.create_all(engine)

    Session = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    session = Session()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
        engine.dispose()
