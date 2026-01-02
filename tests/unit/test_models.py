"""Unit tests for TodoTask model."""

from datetime import datetime

import pytest

from src.domain.models import TodoTask


def test_todo_task_creation():
    """Test TodoTask creation with all fields."""
    now = datetime.now()
    task = TodoTask(
        id=1, description="Buy groceries", is_complete=False, created_at=now
    )

    assert task.id == 1
    assert task.description == "Buy groceries"
    assert task.is_complete is False
    assert task.created_at == now


def test_todo_task_immutability():
    """Test that TodoTask is immutable (frozen dataclass)."""
    task = TodoTask(
        id=1,
        description="Buy groceries",
        is_complete=False,
        created_at=datetime.now(),
    )

    with pytest.raises(Exception):  # FrozenInstanceError
        task.description = "New description"  # type: ignore


def test_todo_task_complete_method():
    """Test that complete() returns a new task with is_complete=True."""
    task = TodoTask(
        id=1,
        description="Buy groceries",
        is_complete=False,
        created_at=datetime.now(),
    )

    completed_task = task.complete()

    # Original task unchanged
    assert task.is_complete is False

    # New task has is_complete=True
    assert completed_task.is_complete is True
    assert completed_task.id == task.id
    assert completed_task.description == task.description
    assert completed_task.created_at == task.created_at


def test_todo_task_complete_idempotent():
    """Test that completing an already complete task works."""
    task = TodoTask(
        id=1,
        description="Buy groceries",
        is_complete=True,
        created_at=datetime.now(),
    )

    completed_task = task.complete()

    assert completed_task.is_complete is True
