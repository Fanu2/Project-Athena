"""
Athena Knowledge Acquisition Exceptions

Compiler-specific exception hierarchy.
"""


class KnowledgeAcquisitionError(Exception):
    """
    Base exception for Athena Knowledge Acquisition.
    """



class PipelineExecutionError(
    KnowledgeAcquisitionError
):
    """
    Raised when a compiler pipeline stage fails.

    Captures:
        - failed stage
        - input type
        - failure message
    """

    def __init__(
        self,
        stage_name: str,
        input_type: str,
        message: str,
    ) -> None:

        self.stage_name = stage_name

        self.input_type = input_type

        self.message = message

        super().__init__(
            self._format_message()
        )

    def _format_message(self) -> str:
        """
        Create readable pipeline failure message.
        """

        return (
            "AKC Pipeline Failed\n\n"
            f"Stage: {self.stage_name}\n"
            f"Input: {self.input_type}\n"
            f"Error: {self.message}"
        )