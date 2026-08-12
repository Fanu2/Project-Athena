"""
Assistant action quality service.
"""

from __future__ import annotations

from .action import (
    AssistantAction,
)

from .action_validation import (
    AssistantActionValidation,
)


class AssistantActionQualityService:
    """
    Validates assistant actions.
    """

    def validate(
        self,
        actions: tuple[
            AssistantAction,
            ...
        ],
    ) -> AssistantActionValidation:
        """
        Validate action definitions.
        """

        checks: list[str] = []

        warnings: list[str] = []

        valid = True

        if not actions:
            return AssistantActionValidation(
                valid=False,
                checks=(),
                warnings=(
                    "no_actions",
                ),
            )

        checks.append(
            "actions_present"
        )

        for action in actions:

            if action.name:

                checks.append(
                    f"{action.name}_named"
                )

            else:

                valid = False

                warnings.append(
                    "unnamed_action"
                )

            if action.description:

                checks.append(
                    f"{action.name}_described"
                )

            else:

                valid = False

                warnings.append(
                    (
                        f"{action.name}"
                        "_missing_description"
                    )
                )

        return AssistantActionValidation(
            valid=valid,
            checks=tuple(checks),
            warnings=tuple(warnings),
        )
