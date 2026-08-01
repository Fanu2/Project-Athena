"""
Compilation report tests.

Validates AKC execution reporting.
"""

from athena.knowledge.acquisition.engine.knowledge_acquisition_engine import (
    KnowledgeAcquisitionEngine,
)


def test_compilation_report_created():

    engine = KnowledgeAcquisitionEngine()

    result, report = (
        engine.compile_with_report(
            "demo.pdf"
        )
    )

    assert report is not None

    assert (
        report.source
        == "demo.pdf"
    )

    assert (
        report.status
        == "success"
    )

    assert (
        report.stage_count
        > 0
    )

    assert (
        report.completed_at
        is not None
    )


def test_compilation_report_tracks_stages():

    engine = KnowledgeAcquisitionEngine()

    _, report = (
        engine.compile_with_report(
            "demo.pdf"
        )
    )

    stage_names = [
        stage.stage_name
        for stage in report.stages
    ]

    assert (
        "import"
        in stage_names
    )

    assert (
        "build"
        in stage_names
    )