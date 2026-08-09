"""
Tests for Athena Knowledge Acquisition Pipeline.
"""

from athena.knowledge.acquisition.engine.knowledge_acquisition_engine import (
    KnowledgeAcquisitionEngine,
)


def test_default_pipeline_execution() -> None:
    """
    Default AKC pipeline executes successfully.
    """

    engine = KnowledgeAcquisitionEngine()

    result = engine.compile(
        "Athena Document",
    )

    assert result is not None


def test_default_pipeline_contains_intelligence_stage() -> None:
    """
    Default pipeline contains document intelligence
    between import and structure processing.
    """

    engine = KnowledgeAcquisitionEngine()

    stages = (
        engine.pass_manager.stages
    )

    names = [
        stage.name
        for stage in stages
    ]

    assert "import" in names

    assert "intelligence" in names

    assert "structure" in names

    assert (
        names.index("intelligence")
        >
        names.index("import")
    )

    assert (
        names.index("intelligence")
        <
        names.index("structure")
    )