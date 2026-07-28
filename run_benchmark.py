from pathlib import Path

from athena.core.application_context import ApplicationContext
from athena.evaluation.benchmark_service import BenchmarkService


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


service = BenchmarkService(
    context.retrieval_service
)


service.run(
    str(dataset),
    output_directory="benchmarks/results/rc2"
)

print("Benchmark completed")