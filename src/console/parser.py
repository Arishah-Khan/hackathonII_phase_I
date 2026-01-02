"""Command parsing utilities.

This module provides command-line input parsing.
"""


def parse_command(user_input: str) -> tuple[str, list[str]]:
    """Parse user input string into command and arguments.

    Args:
        user_input: Raw input string from user

    Returns:
        Tuple of (command_verb, arguments_list)
        - command_verb: First word (lowercased)
        - arguments_list: Remaining words/text as a single joined string in a list
    """
    if not user_input or not user_input.strip():
        return ("", [])

    parts = user_input.strip().split(maxsplit=1)
    command_verb = parts[0].lower()

    if len(parts) > 1:
        # Return arguments as single string (for descriptions with spaces)
        return (command_verb, [parts[1]])
    else:
        return (command_verb, [])
