"""
Assistant action registry.

Maps capabilities to available actions.
"""

from __future__ import annotations

from .action import (
    AssistantAction,
)

from .capability import (
    AssistantCapability,
)


class ActionRegistry:
    """
    Provides controlled action mappings.
    """

    def __init__(self) -> None:

        self._actions = {
            "retrieval": (
                AssistantAction(
                    name="retrieve_information",
                    description=(
                        "Search workspace documents"
                    ),
                ),
            ),

            "summary": (
                AssistantAction(
                    name="retrieve_information",
                    description=(
                        "Search workspace documents"
                    ),
                ),

                AssistantAction(
                    name="build_evidence",
                    description=(
                        "Collect supporting evidence"
                    ),
                ),

                AssistantAction(
                    name="generate_response",
                    description=(
                        "Generate assistant response"
                    ),
                ),

                AssistantAction(
                    name="attach_citations",
                    description=(
                        "Attach source citations"
                    ),
                ),
            ),
        }


    def resolve(
        self,
        capability: AssistantCapability,
    ) -> tuple[
        AssistantAction,
        ...
    ]:
        """
        Resolve capability into actions.
        """

        return self._actions.get(
            capability.name,
            (),
        )
