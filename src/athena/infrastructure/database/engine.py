"""
SQLAlchemy database engine.
"""

from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine

#
# Database location
#

DATABASE_DIR = Path.home() / ".athena"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "athena.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

#
# SQLAlchemy engine
#

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)
