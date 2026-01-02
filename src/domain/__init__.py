"""Domain layer for todo console application.

This module contains core domain models, commands, and validation logic.
All domain logic is decoupled from I/O operations.
"""

from src.domain.commands import CommandRequest, CommandResult, CommandType
from src.domain.models import TodoTask
from src.domain.validation import ValidationResult

__all__ = [
    "CommandRequest",
    "CommandResult",
    "CommandType",
    "TodoTask",
    "ValidationResult",
]
