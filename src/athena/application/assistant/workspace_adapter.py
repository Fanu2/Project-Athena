"""
Assistant workspace integration adapter.
"""

from __future__ import annotations

from athena.services.workspace_query_service import (
    WorkspaceQueryService,
)


class AssistantWorkspaceAdapter:
    """
    Bridges Assistant with workspace services.
    """

    def __init__(
        self,
        workspace_service: WorkspaceQueryService,
    ) -> None:

        self._workspace_service = (
            workspace_service
        )


    def library_summary(
        self,
    ) -> dict[str, int]:
        """
        Return workspace statistics.
        """

        return (
            self._workspace_service
            .library_summary()
        )


    def describe_library(
        self,
    ):
        """
        Return workspace description.
        """

        return (
            self._workspace_service
            .describe_library()
        )
