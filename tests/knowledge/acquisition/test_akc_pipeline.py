from athena.knowledge.acquisition.engine.knowledge_acquisition_engine import (
    KnowledgeAcquisitionEngine,
)


def test_default_pipeline_execution():

    engine = KnowledgeAcquisitionEngine()

    result = engine.compile(
        "Athena Document",
    )

    assert result is not None