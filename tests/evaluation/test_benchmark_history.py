from pathlib import Path

from athena.evaluation.benchmark_history import (
    BenchmarkHistoryStore,
)
from athena.evaluation.benchmark_models import (
    BenchmarkSummary,
)


def test_history_store_saves_summary(
    tmp_path: Path,
) -> None:
    """Benchmark history should persist summaries."""

    store = BenchmarkHistoryStore(
        tmp_path,
    )

    summary = BenchmarkSummary(
        total_questions=10,
        successful_retrievals=9,
        failed_retrievals=1,
        top1_accuracy=0.8,
        top3_accuracy=0.9,
        top5_accuracy=1.0,
        mean_reciprocal_rank=0.85,
        average_latency_ms=120.0,
    )

    path = store.save(
        "Athena Evaluation Suite v1",
        summary,
    )

    assert path.exists()

    history = store.list_history()

    assert len(history) == 1