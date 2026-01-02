"""Unit tests for command parser."""

from src.console.parser import parse_command


def test_parse_command_with_args():
    """Test parsing command with arguments."""
    command, args = parse_command("add Buy groceries")

    assert command == "add"
    assert args == ["Buy groceries"]


def test_parse_command_without_args():
    """Test parsing command without arguments."""
    command, args = parse_command("list")

    assert command == "list"
    assert args == []


def test_parse_command_case_insensitive():
    """Test that command is lowercased."""
    command, args = parse_command("ADD Buy groceries")

    assert command == "add"
    assert args == ["Buy groceries"]


def test_parse_command_whitespace():
    """Test parsing with extra whitespace."""
    command, args = parse_command("  add   Buy groceries  ")

    assert command == "add"
    assert args == ["Buy groceries"]


def test_parse_command_empty():
    """Test parsing empty input."""
    command, args = parse_command("")

    assert command == ""
    assert args == []


def test_parse_command_whitespace_only():
    """Test parsing whitespace-only input."""
    command, args = parse_command("   ")

    assert command == ""
    assert args == []


def test_parse_command_multiword_description():
    """Test parsing command with multi-word description."""
    command, args = parse_command("add Call dentist tomorrow morning")

    assert command == "add"
    assert args == ["Call dentist tomorrow morning"]


def test_parse_command_with_id():
    """Test parsing command with task ID."""
    command, args = parse_command("complete 5")

    assert command == "complete"
    assert args == ["5"]
