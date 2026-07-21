"""
SQLAlchemy model for document checksums.
"""

from __future__ import annotations

from uuid import uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from athena.infrastructure.database.base import Base


class DocumentChecksumModel(Base):
    """Database model for document checksums."""

    __tablename__ = "document_checksums"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    algorithm: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    checksum: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True,
        index=True,
    )

    document_id: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
        index=True,
    )
