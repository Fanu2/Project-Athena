from pathlib import Path

from athena.core.application_context import ApplicationContext
from athena.domain.ai.question import Question
from athena.evaluation.benchmark_loader import BenchmarkLoader


workspace = Path(
    r"C:\Users\singh\Videos\AthenaBenchmarkWorkspace"
)

dataset = Path(
    r".\benchmarks\athena_core_v1.json"
)


context = ApplicationContext()
context.open_workspace(workspace)

questions = BenchmarkLoader.load(dataset)


for question in questions:
    print("=" * 80)
    print(question.question_id)
    print(question.question)

    results = context.retrieval_service.retrieve(
        Question(text=question.question)
    )

    for index, result in enumerate(results[:5], start=1):
        print(
            f"{index}. {result.document_id} "
            f"(score={result.score:.3f})"
        )