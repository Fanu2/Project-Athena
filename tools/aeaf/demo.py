"""
AEAF demonstration runner.
"""

from __future__ import annotations

from pathlib import Path

from tools.aeaf.config import AEAFConfig
from tools.aeaf.engine.pipeline import AnalysisPipeline


def main() -> None:
    """
    Execute the AEAF analysis pipeline.
    """

    project = Path.cwd()

    config = AEAFConfig.default(project)
    config.validate()

    pipeline = AnalysisPipeline(config)

    repository = pipeline.run(
        config.project_root,
    )

    print("Statistics")
    print("-" * 60)

    stats = repository.statistics

    print(f"{'Source Files':20} {stats.source_files}")
    print(f"{'Packages':20} {stats.packages}")
    print(f"{'Modules':20} {stats.modules}")
    print(f"{'Classes':20} {stats.classes}")
    print(f"{'Functions':20} {stats.functions}")
    print(f"{'Methods':20} {stats.methods}")
    print(f"{'Imports':20} {stats.imports}")
    print(f"{'Findings':20} {stats.findings}")

    print()
    print("Dependency Graph")
    print("-" * 60)

    graph = repository.dependency_graph

    print(
        f"{'Edges':20} {len(graph.edges)}"
    )

    print()
    print("Complexity")
    print("-" * 60)

    complexity = repository.complexity

    print(
        f"{'Elements analyzed':20} {len(complexity)}"
    )

    if complexity:

        print()
        print("Top Complexity Hotspots")
        print("-" * 60)

        hotspots = sorted(
            complexity,
            key=lambda item: item.score,
            reverse=True,
        )[:10]

        for index, item in enumerate(
            hotspots,
            start=1,
        ):

            print(
                f"{index:2}. "
                f"{item.name:30} "
                f"{item.score}"
            )

    print()
    print("Documentation")
    print("-" * 60)

    documentation = repository.documentation

    for name, data in documentation.items():

        if isinstance(data, dict):

            print(
                f"{name:20} "
                f"{data.get('documented', 0)}/"
                f"{data.get('total', 0)} "
                f"({data.get('coverage', 0)}%)"
            )


if __name__ == "__main__":
    main()