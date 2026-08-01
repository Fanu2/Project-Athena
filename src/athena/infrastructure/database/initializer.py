"""
Database initialization utilities.
"""

from __future__ import annotations


# Import all models so SQLAlchemy registers them.

from athena.infrastructure.database.models.document_model import (
    DocumentModel,  # noqa: F401
)

from athena.infrastructure.database.models.document_metadata_model import (
    DocumentMetadataModel,  # noqa: F401
)

from athena.infrastructure.database.models.document_checksum_model import (
    DocumentChecksumModel,  # noqa: F401
)

from athena.infrastructure.database.models.document_version_model import (
    DocumentVersionModel,  # noqa: F401
)

from athena.infrastructure.database.models.knowledge_object_model import (
    KnowledgeObjectModel,  # noqa: F401
)


from athena.infrastructure.database.base import Base
from athena.infrastructure.database.engine import engine


def initialize_database() -> None:
    """
    Create all database tables.

    Registered models:
        - Document
        - DocumentMetadata
        - DocumentChecksum
        - DocumentVersion
        - KnowledgeObject
    """

    Base.metadata.create_all(
        bind=engine
    )