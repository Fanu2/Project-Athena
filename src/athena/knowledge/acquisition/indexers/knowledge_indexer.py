"""
Athena Knowledge Indexer Adapter

Bridges canonical KnowledgeObjects
with existing Athena indexing services.
"""

from pathlib import Path
from typing import Any

from ..domain.knowledge_object import (
    KnowledgeObject,
)

from .indexer import Indexer


class KnowledgeIndexer(Indexer):
    """
    Adapter around Athena IndexingService.
    """

    def __init__(
        self,
        indexing_service: Any,
    ) -> None:

        self._indexing_service = indexing_service

    def index(
        self,
        knowledge: KnowledgeObject,
    ) -> Any:
        """
        Index a KnowledgeObject.
        """

        source_path = (
            knowledge.metadata.get(
                "source_path"
            )
        )

        if source_path is None:
            return None

        return self._indexing_service.index_document(
            Path(source_path)
        )