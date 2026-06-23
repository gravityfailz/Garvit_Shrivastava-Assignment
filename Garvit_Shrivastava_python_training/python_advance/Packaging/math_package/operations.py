"""
Question 4 - Packaging

Create a package for
mathematical operations.
"""


def add(first_number: int,
        second_number: int) -> int:
    """
    Return the sum of
    two numbers.
    """

    return first_number + second_number


def subtract(first_number: int,
             second_number: int) -> int:
    """
    Return the difference
    of two numbers.
    """

    return first_number - second_number


def multiply(first_number: int,
             second_number: int) -> int:
    """
    Return the product of
    two numbers.
    """

    return first_number * second_number


def divide(first_number: int,
           second_number: int) -> float:
    """
    Return the division
    result.
    """

    # Prevent division by zero.
    if second_number == 0:
        raise ValueError(
            "Division by zero is not allowed."
        )

    return first_number / second_number