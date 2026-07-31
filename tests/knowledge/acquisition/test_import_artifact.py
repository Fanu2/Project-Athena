from uuid import uuid4

from athena.knowledge.acquisition.domain.import_artifact import (
    ImportArtifact,
)


def test_artifact_creation():

    source_id = uuid4()

    artifact = ImportArtifact(
        source_id=source_id,
        artifact_type="pdf",
        content_reference="paper.pdf",
        checksum="abc123",
    )

    assert artifact.source_id == source_id
    assert artifact.artifact_type == "pdf"
    assert artifact.content_reference == "paper.pdf"
    assert artifact.checksum == "abc123"


def test_artifact_metadata():

    artifact = ImportArtifact()

    artifact.add_metadata(
        "pages",
        10,
    )

    assert artifact.metadata["pages"] == 10