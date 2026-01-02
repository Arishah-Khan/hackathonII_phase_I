"""Main entry point for todo console application.

This module initializes the three agents and starts the REPL.
"""

from src.agents.interface_agent import InterfaceAgent
from src.agents.state_owner import StateOwner
from src.agents.validation_agent import ValidationAgent


def main() -> None:
    """Initialize agents and start the todo console application."""
    # Initialize agents in correct order
    state_owner = StateOwner()
    validator = ValidationAgent(state_owner)
    interface = InterfaceAgent(state_owner, validator)

    # Start the REPL
    interface.run()


if __name__ == "__main__":
    main()
