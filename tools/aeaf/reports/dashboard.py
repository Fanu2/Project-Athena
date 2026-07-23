"""
AEAF dashboard builder.

Coordinates generation of HTML audit dashboards.
"""

from __future__ import annotations

from pathlib import Path

from ..models import RepositoryModel
from .html import HTMLReportGenerator


class DashboardBuilder:
    """
    Build AEAF HTML dashboards.
    """

    def __init__(self) -> None:
        """
        Initialize dashboard builder.
        """

        self.generator = HTMLReportGenerator()


    def build(
        self,
        repository: RepositoryModel,
        output: Path,
    ) -> Path:
        """
        Generate dashboard.

        Parameters
        ----------
        repository
            Audited repository model.

        output
            Destination HTML file.

        Returns
        -------
        Path
            Generated dashboard path.
        """

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.generator.save(
            repository,
            output,
        )

        return output