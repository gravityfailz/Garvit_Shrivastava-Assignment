"""
Question 1
"""


def print_welcome_message() -> None:
    """Print welcome message."""
    print("Welcome to Python Training")


if __name__ == "__main__":
    print_welcome_message()


"""
Question 2
"""

import sys


def display_python_version() -> None:
    """Display installed Python version."""
    print(sys.version)


if __name__ == "__main__":
    display_python_version()