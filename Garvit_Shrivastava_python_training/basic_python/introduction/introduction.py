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

"""
Question 3
"""


def display_user_information() -> None:
    """Display user information."""
    user_name: str = input("Enter name: ")
    user_age: int = int(input("Enter age: "))

    print(f"Hello {user_name}, you are {user_age} years old.")
    

if __name__ == "__main__":
    display_user_information()