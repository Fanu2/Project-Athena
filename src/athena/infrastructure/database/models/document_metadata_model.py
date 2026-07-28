"""
SQLAlchemy model for persistent document metadata.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from athena.infrastructure.database.base import Base

if TYPE_CHECKING:
    from athena.infrastructure.database.models.document_model import DocumentModel


class DocumentMetadataModel(Base):
    """Persistent metadata associated with a document."""

    __tablename__ = "document_metadata"

    document_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("documents.id", ondelete="CASCADE"),
        primary_key=True,
    )

    language: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
    )

    page_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    last_indexed: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    metadata_version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    document: Mapped["DocumentModel"] = relationship(
        "DocumentModel",
        back_populates="document_metadata",
    )

