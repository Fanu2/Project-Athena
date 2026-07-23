"""
AEAF JSON report generator.

Converts RepositoryModel audit results into
a machine-readable JSON report.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..models import RepositoryModel


class JSONReportGenerator:
    """
    Generate JSON audit reports.
    """

    def generate(
        self,
        repository: RepositoryModel,
    ) -> dict[str, Any]:
        """
        Convert repository analysis into report data.
        """

        return {
            "repository": {
                "name": repository.metadata.name,
                "path": str(
                    repository.metadata.root,
                ),
            },

            "statistics": {
                "source_files": (
                    repository.statistics.source_files
                ),
                "packages": (
                    repository.statistics.packages
                ),
                "modules": (
                    repository.statistics.modules
                ),
                "classes": (
                    repository.statistics.classes
                ),
                "functions": (
                    repository.statistics.functions
                ),
                "methods": (
                    repository.statistics.methods
                ),
                "imports": (
                    repository.statistics.imports
                ),
            },

            "dependency_graph": {
                "edges": len(
                    repository.dependency_graph.edges,
                ),
            },

            "complexity": self._complexity_report(
                repository,
            ),

            "documentation": (
                repository.documentation
            ),
        }

    def save(
        self,
        repository: RepositoryModel,
        output: Path,
    ) -> None:
        """
        Save report as JSON file.
        """

        report = self.generate(
            repository,
        )

        output.write_text(
            json.dumps(
                report,
                indent=4,
            ),
            encoding="utf-8",
        )

    def _complexity_report(
        self,
        repository: RepositoryModel,
    ) -> list[dict[str, Any]]:
        """
        Export complexity hotspots.
        """

        hotspots = sorted(
            repository.complexity,
            key=lambda item: item.score,
            reverse=True,
        )[:10]

        return [
            {
                "name": item.name,
                "kind": item.kind,
                "score": item.score,
            }
            for item in hotspots
        ]