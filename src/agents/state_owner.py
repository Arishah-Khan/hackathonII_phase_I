"""State Owner agent implementation.

Agent 1: Manages in-memory task state exclusively.
"""

import random
import string
from datetime import datetime

from src.domain.models import TodoTask


class StateOwner:
    """State Owner agent - manages in-memory task storage.

    Responsibilities:
    - Create new tasks with auto-incrementing IDs
    - Store tasks in memory
    - Retrieve task information
    - Update task completion status
    - Delete tasks from memory

    Prohibitions:
    - No validation logic (delegated to Validation Agent)
    - No user interaction (delegated to Interface Agent)
    - No I/O operations
    """

    def __init__(self) -> None:
        """Initialize state owner with empty task storage."""
        self._tasks: dict[str, TodoTask] = {}

    def _generate_unique_id(self) -> str:
        """Generate a unique 8-character alphanumeric ID.

        Returns:
            Unique ID string (e.g., 'a1b2c3d4')
        """
        while True:
            # Generate 8-character alphanumeric code (lowercase + digits)
            task_id = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=8)
            )
            # Ensure uniqueness
            if task_id not in self._tasks:
                return task_id

    def add_task(self, title: str, description: str) -> str:
        """Create a new task with the given title and description.

        Args:
            title: Task title (already validated)
            description: Task description text (already validated)

        Returns:
            Unique task identifier for the newly created task
        """
        task_id = self._generate_unique_id()
        task = TodoTask(
            id=task_id,
            title=title.strip(),
            description=description.strip(),
            is_complete=False,
            created_at=datetime.now(),
        )
        self._tasks[task_id] = task
        return task_id

    def list_tasks(self) -> list[tuple[str, str, str, bool, datetime]]:
        """Retrieve all tasks currently in memory.

        Returns:
            List of tuples (task_id, title, description, is_complete, created_at)
            Ordered by creation time (chronological order)
        """
        return [
            (task.id, task.title, task.description, task.is_complete, task.created_at)
            for task in sorted(self._tasks.values(), key=lambda t: t.created_at)
        ]

    def complete_task(self, task_id: str) -> bool:
        """Mark a task as complete.

        Args:
            task_id: Identifier of task to mark complete

        Returns:
            True if task was successfully marked complete
            False if task ID not found
        """
        if task_id not in self._tasks:
            return False

        task = self._tasks[task_id]
        if not task.is_complete:
            self._tasks[task_id] = task.complete()
        return True

    def delete_task(self, task_id: str) -> bool:
        """Remove a task from memory.

        Args:
            task_id: Identifier of task to delete

        Returns:
            True if task was successfully deleted
            False if task ID not found
        """
        if task_id not in self._tasks:
            return False

        del self._tasks[task_id]
        return True

    def update_task(self, task_id: str, new_title: str, new_description: str) -> bool:
        """Update a task's title and description.

        Args:
            task_id: Identifier of task to update
            new_title: New title text (already validated)
            new_description: New description text (already validated)

        Returns:
            True if task was successfully updated
            False if task ID not found
        """
        if task_id not in self._tasks:
            return False

        task = self._tasks[task_id]
        updated_task = TodoTask(
            id=task.id,
            title=new_title.strip(),
            description=new_description.strip(),
            is_complete=task.is_complete,
            created_at=task.created_at,
        )
        self._tasks[task_id] = updated_task
        return True

    def get_task(self, task_id: str) -> tuple[str, str, str, bool, datetime] | None:
        """Retrieve a single task by ID.

        Args:
            task_id: Identifier of task to retrieve

        Returns:
            Tuple (task_id, title, description, is_complete, created_at) if found
            None if task does not exist
        """
        task = self._tasks.get(task_id)
        if task is None:
            return None
        return (task.id, task.title, task.description, task.is_complete, task.created_at)

    def get_task_count(self) -> int:
        """Get the current number of tasks in memory.

        Returns:
            Count of tasks currently stored
        """
        return len(self._tasks)
