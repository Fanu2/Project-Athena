from athena.knowledge.acquisition.pipeline.enrichment_pass import (
    EnrichmentPass,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)


def test_enrichment_pass_name():

    stage = EnrichmentPass()

    assert stage.name == "enrichment"


def test_enrichment_pass_execution():

    stage = EnrichmentPass()

    result = stage.execute(
        KnowledgeContext(),
        "knowledge",
    )

    assert result == "knowledge"