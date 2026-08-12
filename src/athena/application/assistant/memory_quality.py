"""
Assistant memory quality service.
"""

from __future__ import annotations

from .memory import (
    AssistantMemoryItem,
)

from .memory_validation import (
    AssistantMemoryValidation,
)


class AssistantMemoryQualityService:
    """
    Validates explicit user-controlled memories.
    """

    def validate(
        self,
        memory: AssistantMemoryItem,
    ) -> AssistantMemoryValidation:
        """
        Validate memory structure.
        """

        checks: list[str] = []
        warnings: list[str] = []

        valid = True

        if memory.key:
            checks.append(
                "key_present"
            )
        else:
            valid = False
            warnings.append(
                "missing_key"
            )

        if memory.value:
            checks.append(
                "value_present"
            )
        else:
            valid = False
            warnings.append(
                "missing_value"
            )

        if memory.source:
            checks.append(
                "source_present"
            )
        else:
            valid = False
            warnings.append(
                "missing_source"
            )

        if memory.scope:
            checks.append(
                "scope_present"
            )
        else:
            valid = False
            warnings.append(
                "missing_scope"
            )

        return AssistantMemoryValidation(
            valid=valid,
            checks=tuple(checks),
            warnings=tuple(warnings),
        )
