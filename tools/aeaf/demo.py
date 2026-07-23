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

    repository = pipeline.run(config.project_root)

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


if __name__ == "__main__":
    main()