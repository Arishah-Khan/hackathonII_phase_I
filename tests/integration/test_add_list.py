"""Integration tests for add and list commands."""

from src.agents.interface_agent import InterfaceAgent
from src.agents.state_owner import StateOwner
from src.agents.validation_agent import ValidationAgent


def test_add_and_list_tasks():
    """Test adding tasks and listing them."""
    # Initialize agents
    state_owner = StateOwner()
    validator = ValidationAgent(state_owner)

    # Add tasks
    task_id1 = state_owner.add_task("Buy groceries")
    task_id2 = state_owner.add_task("Write report")

    # List tasks
    tasks = state_owner.list_tasks()

    # Verify
    assert len(tasks) == 2
    assert tasks[0][0] == task_id1
    assert tasks[0][1] == "Buy groceries"
    assert tasks[0][2] is False  # not complete
    assert tasks[1][0] == task_id2
    assert tasks[1][1] == "Write report"
    assert tasks[1][2] is False


def test_add_task_with_validation():
    """Test adding a task with validation."""
    state_owner = StateOwner()
    validator = ValidationAgent(state_owner)

    # Validate and add valid task
    validation = validator.validate_add_command("Buy groceries")
    assert validation.is_valid is True

    task_id = state_owner.add_task("Buy groceries")
    assert task_id == 1

    # Try to add invalid task (empty description)
    validation = validator.validate_add_command("")
    assert validation.is_valid is False
    assert validation.error_message is not None


def test_empty_list_display():
    """Test listing tasks when none exist."""
    state_owner = StateOwner()

    tasks = state_owner.list_tasks()

    assert tasks == []
