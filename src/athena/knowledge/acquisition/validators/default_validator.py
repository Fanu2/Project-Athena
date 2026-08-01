"""
Athena Default Candidate Validator
"""

from .validator import Validator


class DefaultValidator(Validator):
    """
    Basic deterministic validator.
    """

    def validate(
        self,
        candidate,
    ) -> bool:

        if candidate is None:
            return False

        if candidate.value is None:
            return False

        return True