from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)


def test_context_creation():

    context = KnowledgeContext(
        workspace="research",
        pipeline_name="default",
    )

    assert context.workspace == "research"
    assert context.pipeline_name == "default"


def test_context_options():

    context = KnowledgeContext()

    context.set_option(
        "extract_tables",
        True,
    )

    assert context.options["extract_tables"] is True


def test_provider_selection():

    context = KnowledgeContext()

    context.set_provider(
        "pdf_parser",
        "docling",
    )

    assert (
        context.provider_preferences["pdf_parser"]
        == "docling"
    )