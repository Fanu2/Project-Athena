"""
Athena Knowledge Runtime Factory

Creates fully configured AKC execution contexts.
"""

from ..domain.knowledge_context import (
    KnowledgeContext,
)


class KnowledgeRuntimeFactory:
    """
    Builds KnowledgeContext instances
    with production runtime services.
    """

    def __init__(
        self,
        provider_manager=None,
        knowledge_repository=None,
        knowledge_indexer=None,
        relationship_repository=None,
        evidence_repository=None,
        citation_repository=None,
        evidence_build_service=None,
        citation_build_service=None,
    ) -> None:

        self._services = {
            "provider_manager":
                provider_manager,

            "knowledge_repository":
                knowledge_repository,

            "knowledge_indexer":
                knowledge_indexer,

            "relationship_repository":
                relationship_repository,

            "evidence_repository":
                evidence_repository,

            "citation_repository":
                citation_repository,

            "evidence_build_service":
                evidence_build_service,

            "citation_build_service":
                citation_build_service,
        }

    def create_context(
        self,
    ) -> KnowledgeContext:
        """
        Create configured AKC context.
        """

        context = KnowledgeContext()

        for name, service in (
            self._services.items()
        ):

            if service is not None:

                context.add_service(
                    name,
                    service,
                )

        return context