"""Unit tests for ValidationResult."""

from src.domain.validation import ValidationResult


def test_validation_result_success():
    """Test ValidationResult.success() factory method."""
    result = ValidationResult.success()

    assert result.is_valid is True
    assert result.error_message is None


def test_validation_result_failure():
    """Test ValidationResult.failure() factory method."""
    result = ValidationResult.failure("Test error message")

    assert result.is_valid is False
    assert result.error_message == "Test error message"


def test_validation_result_immutability():
    """Test that ValidationResult is immutable."""
    result = ValidationResult.success()

    # Attempting to modify should raise an error
    try:
        result.is_valid = False  # type: ignore
        assert False, "Should have raised an exception"
    except Exception:
        pass  # Expected
