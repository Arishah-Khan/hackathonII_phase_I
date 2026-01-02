"""Output formatting utilities.

This module provides console output formatting functions.
"""

from datetime import datetime

# Use [X] instead of ✓ for Windows compatibility
TASK_COMPLETE_SYMBOL = "[X]"


def format_task_list(tasks: list[tuple[str, str, str, bool, datetime]]) -> str:
    """Display task list in formatted console output.

    Args:
        tasks: List of task tuples (id, title, description, is_complete, created_at)

    Returns:
        Formatted string for console display
    """
    if not tasks:
        return "No tasks found."

    # Fixed ID width for 8-character UUID-style IDs
    id_width = 8

    # Calculate title width
    title_width = max(len(task[1]) for task in tasks)
    title_width = max(title_width, 5)  # Minimum width for "Title" header
    title_width = min(title_width, 30)  # Maximum width to prevent overly wide tables

    # Calculate description width
    desc_width = max(len(task[2]) for task in tasks)
    desc_width = max(desc_width, 11)  # Minimum width for "Description" header
    desc_width = min(desc_width, 40)  # Maximum width to prevent overly wide tables

    status_width = 8  # "Complete" or "Pending"

    # Create table header
    lines = []
    total_width = id_width + title_width + desc_width + status_width + 13
    lines.append("=" * total_width)
    lines.append(
        f"| {'ID':<{id_width}} | {'Title':<{title_width}} | {'Description':<{desc_width}} | {'Status':<{status_width}} |"
    )
    lines.append("=" * total_width)

    # Add task rows
    for task_id, title, description, is_complete, _ in tasks:
        status = "Complete" if is_complete else "Pending"
        # Truncate title if too long
        if len(title) > title_width:
            title = title[: title_width - 3] + "..."
        # Truncate description if too long
        if len(description) > desc_width:
            description = description[: desc_width - 3] + "..."
        lines.append(
            f"| {task_id:<{id_width}} | {title:<{title_width}} | {description:<{desc_width}} | {status:<{status_width}} |"
        )

    lines.append("=" * total_width)

    return "\n".join(lines)


def format_error(message: str) -> str:
    """Format error message for console display.

    Args:
        message: Error message text

    Returns:
        Formatted error string
    """
    return f"Error: {message}"


def format_success(message: str) -> str:
    """Format success message for console display.

    Args:
        message: Success message text

    Returns:
        Formatted success string
    """
    return message
