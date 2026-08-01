"""
Athena Artifact Adapter

Converts imported artifacts into
Knowledge Representation Models.
"""

from ..domain.import_artifact import ImportArtifact
from ..domain.knowledge_representation import (
    KnowledgeRepresentation,
)


class ArtifactAdapter:
    """
    Converts ImportArtifact into
    KnowledgeRepresentation.
    """

    def adapt(
        self,
        artifact: ImportArtifact,
    ) -> KnowledgeRepresentation:
        """
        Convert imported artifact into KRM.
        """

        representation = KnowledgeRepresentation(
            representation_type=(
                artifact.artifact_type
            ),
            metadata=(
                artifact.metadata.copy()
            ),
        )

        if artifact.content_reference:
            representation.metadata[
                "content_reference"
            ] = artifact.content_reference

        if "title" in artifact.metadata:
            representation.title = (
                artifact.metadata["title"]
            )

        return representation