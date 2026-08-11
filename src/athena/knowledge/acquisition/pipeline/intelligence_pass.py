"""
Athena Document Intelligence Pass.

Runs document understanding after
source representation creation.
"""

from __future__ import annotations

from typing import Any

from ..contracts.pipeline_stage import PipelineStage

from ..domain.knowledge_context import (
    KnowledgeContext,
)

from ..domain.knowledge_representation import (
    KnowledgeRepresentation,
)

from athena.knowledge.intelligence.document_intelligence_service import (
    DocumentIntelligenceService,
)


class IntelligencePass(PipelineStage):
    """
    Generates document intelligence.

    Stores intelligence result in context
    while preserving pipeline flow.
    """

    def __init__(
        self,
        service: DocumentIntelligenceService | None = None,
    ) -> None:

        self._service = (
            service
            if service is not None
            else DocumentIntelligenceService()
        )


    @property
    def name(
        self,
    ) -> str:

        return "intelligence"


    def execute(
        self,
        context: KnowledgeContext,
        input_data: Any,
    ) -> Any:
        """
        Analyze knowledge representation
        and persist document intelligence.
        """

        if not isinstance(
            input_data,
            KnowledgeRepresentation,
        ):
            return input_data


        document = context.get_service(
            "document",
        )

        if document is None:
            return input_data


        intelligence = self._service.analyze(
            document,
            input_data,
        )


        context.add_service(
            "document_intelligence",
            intelligence,
        )


        #
        # Athena Document Intelligence Persistence
        #

        intelligence_repository = (
            context.get_service(
                "document_intelligence_repository",
            )
        )

        if intelligence_repository is not None:

            intelligence_repository.save(
                str(
                    document.id,
                ),
                intelligence,
            )


        #
        # Athena Evidence Persistence
        #

        evidence_service = context.get_service(
            "document_evidence_service",
        )

        if evidence_service is not None:

            evidence_service.build(
                document,
            )


        return input_data
