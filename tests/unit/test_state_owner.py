"""Unit tests for State Owner agent."""

from src.agents.state_owner import StateOwner


def test_add_task():
    """Test adding a task returns correct task ID."""
    state = StateOwner()

    task_id = state.add_task("Buy groceries")

    assert task_id == 1
    assert state.get_task_count() == 1


def test_add_multiple_tasks():
    """Test adding multiple tasks increments IDs."""
    state = StateOwner()

    id1 = state.add_task("Buy groceries")
    id2 = state.add_task("Write report")
    id3 = state.add_task("Call dentist")

    assert id1 == 1
    assert id2 == 2
    assert id3 == 3
    assert state.get_task_count() == 3


def test_list_tasks_empty():
    """Test listing tasks when none exist."""
    state = StateOwner()

    tasks = state.list_tasks()

    assert tasks == []


def test_list_tasks_with_tasks():
    """Test listing tasks returns all tasks in order."""
    state = StateOwner()

    state.add_task("Buy groceries")
    state.add_task("Write report")

    tasks = state.list_tasks()

    assert len(tasks) == 2
    assert tasks[0][0] == 1  # First task ID
    assert tasks[0][1] == "Buy groceries"  # First task description
    assert tasks[1][0] == 2
    assert tasks[1][1] == "Write report"


def test_complete_task():
    """Test marking a task as complete."""
    state = StateOwner()

    task_id = state.add_task("Buy groceries")
    success = state.complete_task(task_id)

    assert success is True

    tasks = state.list_tasks()
    assert tasks[0][2] is True  # is_complete


def test_complete_task_idempotent():
    """Test completing an already complete task succeeds."""
    state = StateOwner()

    task_id = state.add_task("Buy groceries")
    state.complete_task(task_id)
    success = state.complete_task(task_id)  # Complete again

    assert success is True


def test_complete_task_nonexistent():
    """Test completing a non-existent task returns False."""
    state = StateOwner()

    success = state.complete_task(999)

    assert success is False


def test_delete_task():
    """Test deleting a task."""
    state = StateOwner()

    task_id = state.add_task("Buy groceries")
    success = state.delete_task(task_id)

    assert success is True
    assert state.get_task_count() == 0


def test_delete_task_nonexistent():
    """Test deleting a non-existent task returns False."""
    state = StateOwner()

    success = state.delete_task(999)

    assert success is False


def test_delete_task_id_stability():
    """Test that task IDs are not reused after deletion."""
    state = StateOwner()

    id1 = state.add_task("Task 1")
    id2 = state.add_task("Task 2")

    state.delete_task(id1)

    id3 = state.add_task("Task 3")

    # ID 3 should be used, not ID 1
    assert id3 == 3
    assert id3 != id1


def test_get_task():
    """Test retrieving a specific task."""
    state = StateOwner()

    task_id = state.add_task("Buy groceries")
    task = state.get_task(task_id)

    assert task is not None
    assert task[0] == task_id
    assert task[1] == "Buy groceries"
    assert task[2] is False  # is_complete


def test_get_task_nonexistent():
    """Test retrieving a non-existent task returns None."""
    state = StateOwner()

    task = state.get_task(999)

    assert task is None


def test_get_task_count():
    """Test getting task count."""
    state = StateOwner()

    assert state.get_task_count() == 0

    state.add_task("Task 1")
    assert state.get_task_count() == 1

    state.add_task("Task 2")
    assert state.get_task_count() == 2

    state.delete_task(1)
    assert state.get_task_count() == 1
