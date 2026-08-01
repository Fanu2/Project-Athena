"""
Athena Knowledge Workspace Service

Application service exposing compiled
knowledge to Athena workspace features.
"""

from uuid import UUID

from athena.knowledge.acquisition.domain.knowledge_object import (
    KnowledgeObject,
)

from athena.knowledge.models.workspace_knowledge_item import (
    WorkspaceKnowledgeItem,
)

from athena.knowledge.services.knowledge_service import (
    KnowledgeService,
)

from athena.knowledge.services.knowledge_graph_service import (
    KnowledgeGraphService,
)

from athena.knowledge.services.evidence_service import (
    EvidenceService,
)

from athena.knowledge.services.citation_service import (
    CitationService,
)


class KnowledgeWorkspaceService:
    """
    Workspace-facing knowledge API.

    Converts domain knowledge objects
    into UI-friendly read models.

    Exposes:
    - knowledge browsing
    - workspace read models
    - graph relationships
    - evidence lookup
    - citation lookup
    """

    def __init__(
        self,
        knowledge_service: KnowledgeService,
        graph_service: KnowledgeGraphService | None = None,
        evidence_service: EvidenceService | None = None,
        citation_service: CitationService | None = None,
    ) -> None:

        self._knowledge_service = (
            knowledge_service
        )

        self._graph_service = (
            graph_service
        )

        self._evidence_service = (
            evidence_service
        )

        self._citation_service = (
            citation_service
        )

    def list_knowledge(
        self,
    ) -> list[KnowledgeObject]:
        """
        List available knowledge objects.
        """

        return (
            self._knowledge_service
            .list_all()
        )

    def get_knowledge(
        self,
        object_id: UUID,
    ) -> KnowledgeObject | None:
        """
        Retrieve knowledge object.
        """

        return (
            self._knowledge_service
            .get(
                object_id,
            )
        )

    def find_knowledge_by_type(
        self,
        object_type: str,
    ) -> list[KnowledgeObject]:
        """
        Find knowledge by category.
        """

        return (
            self._knowledge_service
            .find_by_type(
                object_type,
            )
        )

    def list_workspace_items(
        self,
    ) -> list[WorkspaceKnowledgeItem]:
        """
        Return UI-ready knowledge items.
        """

        items: list[
            WorkspaceKnowledgeItem
        ] = []

        for obj in self.list_knowledge():

            items.append(
                WorkspaceKnowledgeItem(
                    object_id=obj.object_id,
                    title=obj.title,
                    object_type=obj.object_type,
                    confidence=obj.confidence,
                    source_reference=(
                        obj.metadata.get(
                            "source_reference"
                        )
                    ),
                    provider=(
                        obj.metadata.get(
                            "provider"
                        )
                    ),
                    extraction_method=(
                        obj.metadata.get(
                            "extraction_method"
                        )
                    ),
                )
            )

        return items

    def refresh_workspace_knowledge(
        self,
    ) -> list[WorkspaceKnowledgeItem]:
        """
        Refresh workspace read model.
        """

        return (
            self.list_workspace_items()
        )

    def get_relationships(
        self,
    ):
        """
        Return workspace graph relationships.

        Returns empty list when graph
        service is not configured.
        """

        if self._graph_service is None:
            return []

        return (
            self._graph_service
            .list_relationships()
        )

    def get_evidence(
        self,
        object_id: UUID,
    ):
        """
        Return evidence supporting
        a knowledge object.

        Returns empty list when evidence
        service is not configured.
        """

        if self._evidence_service is None:
            return []

        return (
            self._evidence_service
            .find_by_object(
                object_id,
            )
        )

    def get_citations(
        self,
        evidence_id: UUID,
    ):
        """
        Return citations supporting
        an evidence record.

        Returns empty list when citation
        service is not configured.
        """

        if self._citation_service is None:
            return []

        return (
            self._citation_service
            .find_by_evidence(
                evidence_id,
            )
        )