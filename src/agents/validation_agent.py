"""Validation Agent implementation.

Agent 3: Validates commands and inputs.
"""

from src.agents.state_owner import StateOwner
from src.domain.validation import ValidationResult

# Validation constants
MAX_TITLE_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 500
TASK_ID_LENGTH = 8

# Error messages
ERROR_MISSING_TITLE = "Task title is required"
ERROR_EMPTY_TITLE = "Task title cannot be empty"
ERROR_TITLE_TOO_LONG = "Task title exceeds maximum length of {max_length} characters"
ERROR_EMPTY_DESCRIPTION = "Task description cannot be empty"
ERROR_MISSING_DESCRIPTION = "Task description is required"
ERROR_MISSING_TASK_ID = "Task ID is required for this command"
ERROR_INVALID_TASK_ID_FORMAT = "Task ID must be an 8-character alphanumeric code"
ERROR_TASK_NOT_FOUND = "Task ID '{task_id}' not found"
ERROR_DESCRIPTION_TOO_LONG = (
    "Task description exceeds maximum length of {max_length} characters"
)
ERROR_MISSING_SEPARATOR = "Please use '|' to separate title and description (e.g., 'Title | Description')"


class ValidationAgent:
    """Validation Agent - validates commands before execution.

    Responsibilities:
    - Validate command syntax and format
    - Validate command parameters
    - Check state prerequisites via State Owner queries

    Prohibitions:
    - No state modification (read-only queries only)
    - No user interaction (returns ValidationResult to Interface Agent)
    - No command execution
    """

    def __init__(self, state_owner: StateOwner) -> None:
        """Initialize validation agent.

        Args:
            state_owner: State owner for existence checks
        """
        self._state_owner = state_owner

    def validate_add_command(
        self, title: str | None, description: str | None
    ) -> ValidationResult:
        """Validate an ADD command.

        Args:
            title: Task title to validate
            description: Task description to validate

        Returns:
            ValidationResult indicating success or failure with error message
        """
        if title is None:
            return ValidationResult.failure(ERROR_MISSING_TITLE)

        stripped_title = title.strip()
        if not stripped_title:
            return ValidationResult.failure(ERROR_EMPTY_TITLE)

        if len(stripped_title) > MAX_TITLE_LENGTH:
            return ValidationResult.failure(
                ERROR_TITLE_TOO_LONG.format(max_length=MAX_TITLE_LENGTH)
            )

        if description is None:
            return ValidationResult.failure(ERROR_MISSING_DESCRIPTION)

        stripped_desc = description.strip()
        if not stripped_desc:
            return ValidationResult.failure(ERROR_EMPTY_DESCRIPTION)

        if len(stripped_desc) > MAX_DESCRIPTION_LENGTH:
            return ValidationResult.failure(
                ERROR_DESCRIPTION_TOO_LONG.format(max_length=MAX_DESCRIPTION_LENGTH)
            )

        return ValidationResult.success()

    def validate_complete_command(self, task_id: str | None) -> ValidationResult:
        """Validate a COMPLETE command.

        Args:
            task_id: Task identifier to validate (as string from user input)

        Returns:
            ValidationResult indicating success or failure with error message
        """
        if task_id is None:
            return ValidationResult.failure(ERROR_MISSING_TASK_ID)

        # Validate format: 8-character alphanumeric (lowercase + digits)
        if (
            len(task_id) != TASK_ID_LENGTH
            or not task_id.isalnum()
            or not task_id.islower()
        ):
            return ValidationResult.failure(ERROR_INVALID_TASK_ID_FORMAT)

        if self._state_owner.get_task(task_id) is None:
            return ValidationResult.failure(ERROR_TASK_NOT_FOUND.format(task_id=task_id))

        return ValidationResult.success()

    def validate_delete_command(self, task_id: str | None) -> ValidationResult:
        """Validate a DELETE command.

        Args:
            task_id: Task identifier to validate (as string from user input)

        Returns:
            ValidationResult indicating success or failure with error message
        """
        if task_id is None:
            return ValidationResult.failure(ERROR_MISSING_TASK_ID)

        # Validate format: 8-character alphanumeric (lowercase + digits)
        if (
            len(task_id) != TASK_ID_LENGTH
            or not task_id.isalnum()
            or not task_id.islower()
        ):
            return ValidationResult.failure(ERROR_INVALID_TASK_ID_FORMAT)

        if self._state_owner.get_task(task_id) is None:
            return ValidationResult.failure(ERROR_TASK_NOT_FOUND.format(task_id=task_id))

        return ValidationResult.success()

    def validate_update_command(
        self, task_id: str | None, title: str | None, description: str | None
    ) -> ValidationResult:
        """Validate an UPDATE command.

        Args:
            task_id: Task identifier to validate (as string from user input)
            title: New title to validate
            description: New description to validate

        Returns:
            ValidationResult indicating success or failure with error message
        """
        if task_id is None:
            return ValidationResult.failure(ERROR_MISSING_TASK_ID)

        # Validate format: 8-character alphanumeric (lowercase + digits)
        if (
            len(task_id) != TASK_ID_LENGTH
            or not task_id.isalnum()
            or not task_id.islower()
        ):
            return ValidationResult.failure(ERROR_INVALID_TASK_ID_FORMAT)

        if self._state_owner.get_task(task_id) is None:
            return ValidationResult.failure(ERROR_TASK_NOT_FOUND.format(task_id=task_id))

        if title is None:
            return ValidationResult.failure(ERROR_MISSING_TITLE)

        stripped_title = title.strip()
        if not stripped_title:
            return ValidationResult.failure(ERROR_EMPTY_TITLE)

        if len(stripped_title) > MAX_TITLE_LENGTH:
            return ValidationResult.failure(
                ERROR_TITLE_TOO_LONG.format(max_length=MAX_TITLE_LENGTH)
            )

        if description is None:
            return ValidationResult.failure(ERROR_MISSING_DESCRIPTION)

        stripped_desc = description.strip()
        if not stripped_desc:
            return ValidationResult.failure(ERROR_EMPTY_DESCRIPTION)

        if len(stripped_desc) > MAX_DESCRIPTION_LENGTH:
            return ValidationResult.failure(
                ERROR_DESCRIPTION_TOO_LONG.format(max_length=MAX_DESCRIPTION_LENGTH)
            )

        return ValidationResult.success()

    def validate_list_command(self) -> ValidationResult:
        """Validate a LIST command.

        Returns:
            ValidationResult with is_valid=True (always succeeds)
        """
        return ValidationResult.success()

    def validate_help_command(self) -> ValidationResult:
        """Validate a HELP command.

        Returns:
            ValidationResult with is_valid=True (always succeeds)
        """
        return ValidationResult.success()

    def validate_exit_command(self) -> ValidationResult:
        """Validate an EXIT command.

        Returns:
            ValidationResult with is_valid=True (always succeeds)
        """
        return ValidationResult.success()
