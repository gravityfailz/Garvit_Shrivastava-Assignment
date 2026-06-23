"""
Question 1 - Packaging

Import utility functions
from another module.
"""

from number_utils import (
    get_cube,
    get_square,
)


def display_results() -> None:
    """
    Display utility
    function results.
    """

    number = int(input("Enter a number: "))

    print(f"Square: {get_square(number)}")
    print(f"Cube: {get_cube(number)}")


if __name__ == "__main__":
    display_results()