"""Validation result types for todo console application.

This module defines validation outcomes from the Validation Agent.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationResult:
    """Result of command validation.

    Attributes:
        is_valid: Whether the command passed validation
        error_message: Error description if validation failed
    """

    is_valid: bool
    error_message: str | None = None

    @staticmethod
    def success() -> "ValidationResult":
        """Create a successful validation result.

        Returns:
            ValidationResult with is_valid=True
        """
        return ValidationResult(is_valid=True)

    @staticmethod
    def failure(message: str) -> "ValidationResult":
        """Create a failed validation result with error message.

        Args:
            message: Human-readable error description

        Returns:
            ValidationResult with is_valid=False and error message
        """
        return ValidationResult(is_valid=False, error_message=message)
