"""
Question 4 - Packaging

Use the mathematical
operations package.
"""

from operations import (
    add,
    divide,
    multiply,
    subtract,
)


def display_results() -> None:
    """
    Display operation results.
    """

    first_number = float(input("Enter first number: "))
    second_number = float(input("Enter second number: "))

    print(f"Addition: {add(first_number, second_number)}")
    print(
        f"Subtraction: "
        f"{subtract(first_number, second_number)}"
    )
    print(
        f"Multiplication: "
        f"{multiply(first_number, second_number)}"
    )
    print(
        f"Division: "
        f"{divide(first_number, second_number)}"
    )


if __name__ == "__main__":
    display_results()