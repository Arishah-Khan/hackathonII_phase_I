"""
Validation Agent Interface Contract

This module defines the interface contract for Agent 3 (Validation Agent).
The Validation Agent is responsible for:
- Validating command syntax and format
- Validating command parameters (non-empty description, valid task ID)
- Checking state prerequisites (task existence for complete/delete)

The Validation Agent MUST NOT:
- Modify state (delegated to State Owner)
- Interact with users directly (delegated to Interface Agent)
- Execute commands (only validates them)

All validation occurs before command execution.
"""

from typing import Protocol
from dataclasses import dataclass
from enum import Enum


class CommandType(Enum):
    """Supported command types."""
    ADD = "add"
    LIST = "list"
    COMPLETE = "complete"
    DELETE = "delete"
    HELP = "help"
    EXIT = "exit"


@dataclass(frozen=True)
class ValidationResult:
    """Result of command validation.

    Attributes:
        is_valid: Whether the command passed all validation checks
        error_message: Human-readable error description (present if is_valid=False)
    """
    is_valid: bool
    error_message: str | None = None

    @staticmethod
    def success() -> 'ValidationResult':
        """Create a successful validation result."""
        return ValidationResult(is_valid=True)

    @staticmethod
    def failure(message: str) -> 'ValidationResult':
        """Create a failed validation result.

        Args:
            message: Human-readable error description

        Returns:
            ValidationResult with is_valid=False and error message
        """
        return ValidationResult(is_valid=False, error_message=message)


class ValidationAgentInterface(Protocol):
    """Protocol defining the Validation Agent's public interface.

    The Validation Agent validates commands before execution but does not
    modify state or interact with users.
    """

    def validate_add_command(self, description: str | None) -> ValidationResult:
        """Validate an ADD command.

        Validation Rules:
            - description must be provided (not None)
            - description must be non-empty after trimming whitespace
            - description length reasonable (prevent abuse)

        Args:
            description: Task description to validate

        Returns:
            ValidationResult indicating success or failure with error message

        Example:
            >>> result = validator.validate_add_command("Buy groceries")
            >>> result.is_valid
            True

            >>> result = validator.validate_add_command("")
            >>> result.is_valid
            False
            >>> result.error_message
            "Task description cannot be empty"
        """
        ...

    def validate_complete_command(self, task_id: str | None) -> ValidationResult:
        """Validate a COMPLETE command.

        Validation Rules:
            - task_id must be provided (not None)
            - task_id must be valid integer format
            - task_id must be positive
            - task_id must exist in state (checked via State Owner query)

        Args:
            task_id: Task identifier to validate (as string from user input)

        Returns:
            ValidationResult indicating success or failure with error message

        Example:
            >>> result = validator.validate_complete_command("1")
            >>> result.is_valid
            True

            >>> result = validator.validate_complete_command("abc")
            >>> result.is_valid
            False
            >>> result.error_message
            "Task ID must be a number"
        """
        ...

    def validate_delete_command(self, task_id: str | None) -> ValidationResult:
        """Validate a DELETE command.

        Validation Rules:
            - task_id must be provided (not None)
            - task_id must be valid integer format
            - task_id must be positive
            - task_id must exist in state (checked via State Owner query)

        Args:
            task_id: Task identifier to validate (as string from user input)

        Returns:
            ValidationResult indicating success or failure with error message

        Example:
            >>> result = validator.validate_delete_command("1")
            >>> result.is_valid
            True

            >>> result = validator.validate_delete_command("999")
            >>> result.is_valid
            False
            >>> result.error_message
            "Task ID '999' not found"
        """
        ...

    def validate_list_command(self) -> ValidationResult:
        """Validate a LIST command.

        LIST command has no parameters, so always succeeds.

        Returns:
            ValidationResult with is_valid=True

        Example:
            >>> result = validator.validate_list_command()
            >>> result.is_valid
            True
        """
        ...

    def validate_help_command(self) -> ValidationResult:
        """Validate a HELP command.

        HELP command has no parameters, so always succeeds.

        Returns:
            ValidationResult with is_valid=True

        Example:
            >>> result = validator.validate_help_command()
            >>> result.is_valid
            True
        """
        ...

    def validate_exit_command(self) -> ValidationResult:
        """Validate an EXIT command.

        EXIT command has no parameters, so always succeeds.

        Returns:
            ValidationResult with is_valid=True

        Example:
            >>> result = validator.validate_exit_command()
            >>> result.is_valid
            True
        """
        ...


# Interface contract specification
CONTRACT_VERSION = "1.0.0"
CONTRACT_DESCRIPTION = "Validation Agent interface for command validation"

# Validation error messages (standardized)
ERROR_EMPTY_DESCRIPTION = "Task description cannot be empty"
ERROR_MISSING_DESCRIPTION = "Task description is required for 'add' command"
ERROR_MISSING_TASK_ID = "Task ID is required for this command"
ERROR_INVALID_TASK_ID_FORMAT = "Task ID must be a number"
ERROR_NEGATIVE_TASK_ID = "Task ID must be a positive number"
ERROR_TASK_NOT_FOUND = "Task ID '{task_id}' not found"
ERROR_DESCRIPTION_TOO_LONG = "Task description exceeds maximum length of {max_length} characters"

# Validation constraints
MAX_DESCRIPTION_LENGTH = 500  # Prevent abuse with extremely long descriptions
MIN_TASK_ID = 1  # Task IDs start at 1

# Constitutional compliance notes:
# - No state modification (read-only queries to State Owner for existence checks)
# - No I/O operations (validation results returned to Interface Agent)
# - Type hints on all methods (constitutional requirement)
# - Immutable ValidationResult (frozen dataclass)
