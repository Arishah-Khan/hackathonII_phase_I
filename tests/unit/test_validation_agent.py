"""Unit tests for Validation Agent."""

from src.agents.state_owner import StateOwner
from src.agents.validation_agent import ValidationAgent


def test_validate_add_command_valid():
    """Test validating a valid ADD command."""
    state = StateOwner()
    validator = ValidationAgent(state)

    result = validator.validate_add_command("Buy groceries")

    assert result.is_valid is True
    assert result.error_message is None


def test_validate_add_command_empty():
    """Test validating ADD command with empty description."""
    state = StateOwner()
    validator = ValidationAgent(state)

    result = validator.validate_add_command("")

    assert result.is_valid is False
    assert "cannot be empty" in result.error_message or ""


def test_validate_add_command_none():
    """Test validating ADD command with None description."""
    state = StateOwner()
    validator = ValidationAgent(state)

    result = validator.validate_add_command(None)

    assert result.is_valid is False
    assert "required" in result.error_message or ""


def test_validate_add_command_whitespace():
    """Test validating ADD command with whitespace-only description."""
    state = StateOwner()
    validator = ValidationAgent(state)

    result = validator.validate_add_command("   ")

    assert result.is_valid is False
    assert "cannot be empty" in result.error_message or ""


def test_validate_add_command_too_long():
    """Test validating ADD command with description exceeding max length."""
    state = StateOwner()
    validator = ValidationAgent(state)

    long_description = "a" * 501  # Exceeds MAX_DESCRIPTION_LENGTH (500)
    result = validator.validate_add_command(long_description)

    assert result.is_valid is False
    assert "exceeds maximum length" in result.error_message or ""


def test_validate_complete_command_valid():
    """Test validating a valid COMPLETE command."""
    state = StateOwner()
    state.add_task("Buy groceries")
    validator = ValidationAgent(state)

    result = validator.validate_complete_command("1")

    assert result.is_valid is True


def test_validate_complete_command_none():
    """Test validating COMPLETE command with None task ID."""
    state = StateOwner()
    validator = ValidationAgent(state)

    result = validator.validate_complete_command(None)

    assert result.is_valid is False
    assert "required" in result.error_message or ""


def test_validate_complete_command_invalid_format():
    """Test validating COMPLETE command with non-numeric task ID."""
    state = StateOwner()
    validator = ValidationAgent(state)

    result = validator.validate_complete_command("abc")

    assert result.is_valid is False
    assert "must be a number" in result.error_message or ""


def test_validate_complete_command_negative():
    """Test validating COMPLETE command with negative task ID."""
    state = StateOwner()
    validator = ValidationAgent(state)

    result = validator.validate_complete_command("-1")

    assert result.is_valid is False
    assert "positive" in result.error_message or ""


def test_validate_complete_command_nonexistent():
    """Test validating COMPLETE command with non-existent task ID."""
    state = StateOwner()
    validator = ValidationAgent(state)

    result = validator.validate_complete_command("999")

    assert result.is_valid is False
    assert "not found" in result.error_message or ""


def test_validate_delete_command_valid():
    """Test validating a valid DELETE command."""
    state = StateOwner()
    state.add_task("Buy groceries")
    validator = ValidationAgent(state)

    result = validator.validate_delete_command("1")

    assert result.is_valid is True


def test_validate_delete_command_nonexistent():
    """Test validating DELETE command with non-existent task ID."""
    state = StateOwner()
    validator = ValidationAgent(state)

    result = validator.validate_delete_command("999")

    assert result.is_valid is False
    assert "not found" in result.error_message or ""


def test_validate_list_command():
    """Test validating LIST command always succeeds."""
    state = StateOwner()
    validator = ValidationAgent(state)

    result = validator.validate_list_command()

    assert result.is_valid is True


def test_validate_help_command():
    """Test validating HELP command always succeeds."""
    state = StateOwner()
    validator = ValidationAgent(state)

    result = validator.validate_help_command()

    assert result.is_valid is True


def test_validate_exit_command():
    """Test validating EXIT command always succeeds."""
    state = StateOwner()
    validator = ValidationAgent(state)

    result = validator.validate_exit_command()

    assert result.is_valid is True
