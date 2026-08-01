"""
Knowledge compilation service tests.
"""

from athena.knowledge.services.knowledge_compilation_service import (
    KnowledgeCompilationService,
)

from athena.knowledge.acquisition.engine.knowledge_acquisition_engine import (
    KnowledgeAcquisitionEngine,
)


def test_compilation_service_creation():

    service = (
        KnowledgeCompilationService(
            KnowledgeAcquisitionEngine()
        )
    )

    assert service is not None