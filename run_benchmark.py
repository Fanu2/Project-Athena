from pathlib import Path

from athena.ai.retrieval.hybrid_ranker import (
    HybridRanker,
)
from athena.ai.retrieval.ranking import (
    CandidateScorer,
)
from athena.ai.retrieval.ranking_profiles import (
    AUTHORITY_EXPERIMENT_PROFILE,
)
from athena.application.ai.retrieval_service import (
    RetrievalService,
)
from athena.core.application_context import (
    ApplicationContext,
)
from athena.evaluation.benchmark_service import (
    BenchmarkService,
)


workspace = Path(
    r"C:\Users\singh\Videos\AthenaBenchmarkWorkspace"
)

dataset = Path(
    r"benchmarks\athena_core_v1.json"
)


context = ApplicationContext()

context.open_workspace(
    workspace
)


authority_ranker = HybridRanker(
    scorer=CandidateScorer(
        profile=AUTHORITY_EXPERIMENT_PROFILE,
    )
)


semantic_service = (
    context.retrieval_service.semantic_retrieval_service
)

semantic_service.set_hybrid_ranker(
    authority_ranker
)


context.retrieval_service = RetrievalService(
    semantic_retrieval_service=semantic_service,
)


service = BenchmarkService(
    context.retrieval_service
)


service.run(
    str(dataset),
    output_directory="benchmarks/results/rc2-authority",
)

print("Benchmark completed")