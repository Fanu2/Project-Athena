"""
Athena Build Pass

Creates canonical Knowledge Objects
from validated candidates.
"""

from typing import Any

from ..contracts.pipeline_stage import PipelineStage
from ..domain.knowledge_context import KnowledgeContext
from ..domain.knowledge_candidate import (
    KnowledgeCandidate,
)
from ..domain.knowledge_object import (
    KnowledgeObject,
)


class BuildPass(PipelineStage):
    """
    Converts validated candidates into
    canonical Athena knowledge objects.

    Optional execution context services:

    - knowledge_repository:
        persists created knowledge objects

    - evidence_build_service:
        creates provenance evidence

    - citation_build_service:
        creates citations from evidence
    """

    @property
    def name(self) -> str:
        return "build"

    def execute(
        self,
        context: KnowledgeContext,
        input_data: Any,
    ) -> Any:
        """
        Build canonical knowledge objects.
        """

        if not isinstance(
            input_data,
            list,
        ):
            return input_data

        knowledge_repository = (
            context.get_service(
                "knowledge_repository"
            )
        )

        evidence_builder = (
            context.get_service(
                "evidence_build_service"
            )
        )

        citation_builder = (
            context.get_service(
                "citation_build_service"
            )
        )

        print(
            "BUILD PASS REPOSITORY:",
            knowledge_repository,
        )

        print(
            "EVIDENCE BUILDER:",
            evidence_builder,
        )

        print(
            "CITATION BUILDER:",
            citation_builder,
        )

        objects: list[KnowledgeObject] = []

        for candidate in input_data:

            if not isinstance(
                candidate,
                KnowledgeCandidate,
            ):
                continue

            knowledge_object = KnowledgeObject(
                object_type=(
                    candidate.candidate_type
                ),
                title=candidate.value,
                confidence=(
                    candidate.confidence
                ),
                metadata=(
                    candidate.metadata.copy()
                ),
            )

            knowledge_object.update_metadata(
                "source_candidate_id",
                str(
                    candidate.candidate_id
                ),
            )

            print(
                "BUILDING KNOWLEDGE OBJECT:",
                knowledge_object.title,
            )

            #
            # Persist knowledge object
            #

            if knowledge_repository is not None:

                try:

                    knowledge_repository.save(
                        knowledge_object
                    )

                    print(
                        "KNOWLEDGE OBJECT PERSISTED:",
                        knowledge_object.object_id,
                    )

                except Exception as exc:

                    print(
                        "KNOWLEDGE SAVE FAILED:",
                        type(exc).__name__,
                        str(exc),
                    )

                    raise

            else:

                print(
                    "WARNING: No knowledge repository configured"
                )

            #
            # Build provenance evidence
            #

            evidence = None

            if evidence_builder is not None:

                print(
                    "BUILDING EVIDENCE:",
                    knowledge_object.title,
                )

                evidence = (
                    evidence_builder.build(
                        knowledge_object
                    )
                )

                print(
                    "EVIDENCE CREATED:",
                    evidence,
                )

            else:

                print(
                    "WARNING: No evidence builder configured"
                )

            #
            # Build citation from evidence
            #

            if (
                evidence is not None
                and citation_builder is not None
            ):

                print(
                    "BUILDING CITATION"
                )

                citation_builder.build(
                    evidence
                )

            elif citation_builder is None:

                print(
                    "WARNING: No citation builder configured"
                )

            objects.append(
                knowledge_object
            )

        print(
            "BUILD PASS CREATED OBJECTS:",
            len(objects),
        )

        return objects