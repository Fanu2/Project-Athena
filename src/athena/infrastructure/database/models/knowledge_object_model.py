"""
Athena Knowledge Object Database Model
"""

from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    Text,
)

from sqlalchemy.dialects.sqlite import JSON

from athena.infrastructure.database.base import Base


class KnowledgeObjectModel(Base):
    """
    Persistent Knowledge Object.
    """

    __tablename__ = "knowledge_objects"

    object_id = Column(
        String,
        primary_key=True,
    )

    object_type = Column(
        String,
        nullable=False,
    )

    title = Column(
        String,
        nullable=True,
    )

    content = Column(
        Text,
        nullable=True,
    )

    metadata_json = Column(
        JSON,
        nullable=False,
        default=dict,
    )

    confidence = Column(
        Float,
        nullable=False,
        default=1.0,
    )

    created_at = Column(
        DateTime,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        nullable=False,
    )