"""Unit tests for output formatter."""

from datetime import datetime

from src.console.formatter import format_error, format_success, format_task_list


def test_format_task_list_with_tasks():
    """Test formatting task list with multiple tasks."""
    tasks = [
        (1, "Buy groceries", False, datetime.now()),
        (2, "Write report", True, datetime.now()),
        (3, "Call dentist", False, datetime.now()),
    ]

    result = format_task_list(tasks)

    # Check for table format elements
    assert "ID" in result
    assert "Description" in result
    assert "Status" in result
    assert "Buy groceries" in result
    assert "Write report" in result
    assert "Call dentist" in result
    assert "Pending" in result
    assert "Complete" in result
    assert "|" in result  # Table border
    assert "=" in result  # Table separator


def test_format_task_list_empty():
    """Test formatting empty task list."""
    result = format_task_list([])

    assert result == "No tasks found."


def test_format_task_list_all_complete():
    """Test formatting task list with all completed tasks."""
    tasks = [
        (1, "Buy groceries", True, datetime.now()),
        (2, "Write report", True, datetime.now()),
    ]

    result = format_task_list(tasks)

    # Check that all tasks show as complete in table format
    assert "Complete" in result
    assert "Buy groceries" in result
    assert "Write report" in result
    # Verify no pending status for completed tasks
    lines = result.split("\n")
    task_lines = [line for line in lines if "Buy groceries" in line or "Write report" in line]
    for line in task_lines:
        assert "Complete" in line


def test_format_error():
    """Test error message formatting."""
    result = format_error("Task not found")

    assert result == "Error: Task not found"


def test_format_success():
    """Test success message formatting."""
    result = format_success("Task added successfully")

    assert result == "Task added successfully"
