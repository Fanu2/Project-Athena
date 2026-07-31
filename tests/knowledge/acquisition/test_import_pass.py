from athena.knowledge.acquisition.pipeline.import_pass import (
    ImportPass,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)


def test_import_pass_name():

    stage = ImportPass()

    assert stage.name == "import"


def test_import_pass_execution():

    stage = ImportPass()

    result = stage.execute(
        KnowledgeContext(),
        "document",
    )

    assert result == "document"