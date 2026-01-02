"""Domain models for todo console application.

This module defines the core TodoTask entity.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TodoTask:
    """Immutable representation of a todo task.

    Attributes:
        id: Unique task identifier (UUID-style alphanumeric code)
        title: Task title (brief summary)
        description: Task description text (detailed information)
        is_complete: Whether task has been marked complete
        created_at: Timestamp when task was created
    """

    id: str
    title: str
    description: str
    is_complete: bool
    created_at: datetime

    def complete(self) -> "TodoTask":
        """Return new task with is_complete=True.

        Returns:
            New TodoTask instance with completion status updated
        """
        return TodoTask(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=True,
            created_at=self.created_at,
        )
