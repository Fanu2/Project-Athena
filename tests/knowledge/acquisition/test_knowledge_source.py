from athena.knowledge.acquisition.domain.knowledge_source import (
    KnowledgeSource,
)


def test_source_creation():

    source = KnowledgeSource(
        name="Athena Research Paper",
        source_type="pdf",
        location="research/paper.pdf",
    )

    assert source.name == "Athena Research Paper"
    assert source.source_type == "pdf"
    assert source.location == "research/paper.pdf"


def test_source_metadata():

    source = KnowledgeSource()

    source.add_metadata(
        "author",
        "OpenAI",
    )

    assert source.metadata["author"] == "OpenAI"