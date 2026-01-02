"""Command types and data structures for todo console application.

This module defines commands that flow between agents.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class CommandType(Enum):
    """Supported command operations."""

    ADD = "add"
    LIST = "list"
    COMPLETE = "complete"
    DELETE = "delete"
    HELP = "help"
    EXIT = "exit"


@dataclass(frozen=True)
class CommandRequest:
    """Represents a parsed and validated user command.

    Attributes:
        command_type: The type of command operation
        task_id: Task identifier (for COMPLETE/DELETE commands)
        description: Task description (for ADD commands)
    """

    command_type: CommandType
    task_id: int | None = None
    description: str | None = None


@dataclass(frozen=True)
class CommandResult:
    """Result of command execution.

    Attributes:
        success: Whether command executed successfully
        message: User-facing success or error message
        tasks: List of tasks (for LIST command)
    """

    success: bool
    message: str | None = None
    tasks: list[tuple[int, str, bool, datetime]] | None = None
