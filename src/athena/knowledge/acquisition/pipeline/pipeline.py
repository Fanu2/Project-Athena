"""
Athena Knowledge Compiler Pipeline

Creates the default AKC execution pipeline.
"""

from ..engine.pass_manager import PassManager

from .import_pass import ImportPass
from .intelligence_pass import IntelligencePass
from .structure_pass import StructurePass
from .semantic_pass import SemanticPass
from .relationship_pass import RelationshipPass
from .validation_pass import ValidationPass
from .enrichment_pass import EnrichmentPass
from .build_pass import BuildPass
from .index_pass import IndexPass


def create_default_pipeline() -> PassManager:
    """
    Create standard Athena compiler pipeline.

    Note:
        RelationshipBuildPass is intentionally not part
        of the default linear pipeline yet.

        Relationship compilation requires branching
        support because relationships are a parallel
        knowledge artifact and should not replace the
        main KnowledgeCandidate stream.
    """

    manager = PassManager()

    manager.register(
        ImportPass()
    )

    manager.register(
        IntelligencePass()
    )

    manager.register(
        StructurePass()
    )

    manager.register(
        SemanticPass()
    )

    manager.register(
        RelationshipPass()
    )

    manager.register(
        ValidationPass()
    )

    manager.register(
        EnrichmentPass()
    )

    manager.register(
        BuildPass()
    )

    manager.register(
        IndexPass()
    )

    return manager