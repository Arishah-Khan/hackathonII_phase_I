"""
State Owner Agent Interface Contract

This module defines the interface contract for Agent 1 (State Owner).
The State Owner is responsible for:
- Managing in-memory task state (create, read, update, delete)
- Maintaining task ID allocation
- Enforcing state invariants

The State Owner MUST NOT:
- Perform validation (delegated to Validation Agent)
- Interact with users directly (delegated to Interface Agent)
- Perform I/O operations

All methods assume pre-validated input from Validation Agent.
"""

from typing import Protocol, List
from datetime import datetime


# Type aliases for clarity
TaskId = int
TaskDescription = str


class StateOwnerInterface(Protocol):
    """Protocol defining the State Owner agent's public interface.

    This protocol uses structural typing to define the contract that
    State Owner implementations must satisfy.
    """

    def add_task(self, description: TaskDescription) -> TaskId:
        """Create a new task with the given description.

        Preconditions:
            - description is non-empty (validated by Validation Agent)

        Postconditions:
            - New task created with unique ID
            - Task added to internal state
            - Task ID counter incremented

        Args:
            description: Task description text (already validated)

        Returns:
            Unique task identifier for the newly created task

        Example:
            >>> task_id = state_owner.add_task("Buy groceries")
            >>> task_id
            1
        """
        ...

    def list_tasks(self) -> List[tuple[TaskId, TaskDescription, bool, datetime]]:
        """Retrieve all tasks currently in memory.

        Postconditions:
            - Returns snapshot of current state (no side effects)
            - Empty list if no tasks exist

        Returns:
            List of tuples (task_id, description, is_complete, created_at)
            Ordered by task ID (chronological creation order)

        Example:
            >>> tasks = state_owner.list_tasks()
            >>> tasks
            [(1, "Buy groceries", False, datetime(2026, 1, 1, 10, 0, 0)),
             (2, "Write report", True, datetime(2026, 1, 1, 10, 5, 0))]
        """
        ...

    def complete_task(self, task_id: TaskId) -> bool:
        """Mark a task as complete.

        Preconditions:
            - task_id exists (validated by Validation Agent)

        Postconditions:
            - Task's is_complete flag set to True
            - Idempotent: marking complete task as complete succeeds

        Args:
            task_id: Identifier of task to mark complete

        Returns:
            True if task was successfully marked complete
            False if task ID not found (should not happen with validation)

        Example:
            >>> success = state_owner.complete_task(1)
            >>> success
            True
        """
        ...

    def delete_task(self, task_id: TaskId) -> bool:
        """Remove a task from memory.

        Preconditions:
            - task_id exists (validated by Validation Agent)

        Postconditions:
            - Task removed from internal state
            - Task ID not reused for new tasks

        Args:
            task_id: Identifier of task to delete

        Returns:
            True if task was successfully deleted
            False if task ID not found (should not happen with validation)

        Example:
            >>> success = state_owner.delete_task(1)
            >>> success
            True
        """
        ...

    def get_task(self, task_id: TaskId) -> tuple[TaskId, TaskDescription, bool, datetime] | None:
        """Retrieve a single task by ID.

        Used by Validation Agent to check task existence.

        Args:
            task_id: Identifier of task to retrieve

        Returns:
            Tuple (task_id, description, is_complete, created_at) if found
            None if task does not exist

        Example:
            >>> task = state_owner.get_task(1)
            >>> task
            (1, "Buy groceries", False, datetime(2026, 1, 1, 10, 0, 0))
        """
        ...

    def get_task_count(self) -> int:
        """Get the current number of tasks in memory.

        Returns:
            Count of tasks currently stored

        Example:
            >>> count = state_owner.get_task_count()
            >>> count
            5
        """
        ...


# Interface contract specification
CONTRACT_VERSION = "1.0.0"
CONTRACT_DESCRIPTION = "State Owner Agent interface for in-memory task management"

# Constitutional compliance notes:
# - No I/O operations (console-only interface delegated to Interface Agent)
# - No validation logic (delegated to Validation Agent)
# - In-memory only (no persistence methods)
# - Immutable return types (tuples) for task data
# - Type hints on all methods (constitutional requirement)
