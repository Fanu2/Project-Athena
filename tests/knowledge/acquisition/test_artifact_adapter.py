from athena.knowledge.acquisition.adapters.artifact_adapter import (
    ArtifactAdapter,
)

from athena.knowledge.acquisition.domain.import_artifact import (
    ImportArtifact,
)


def test_artifact_adapter_creates_representation():

    artifact = ImportArtifact(
        artifact_type="document",
        content_reference="test.pdf",
    )

    artifact.add_metadata(
        "title",
        "Athena Test",
    )

    result = ArtifactAdapter().adapt(
        artifact
    )

    assert (
        result.representation_type
        == "document"
    )

    assert (
        result.title
        == "Athena Test"
    )

    assert (
        result.metadata["content_reference"]
        == "test.pdf"
    )