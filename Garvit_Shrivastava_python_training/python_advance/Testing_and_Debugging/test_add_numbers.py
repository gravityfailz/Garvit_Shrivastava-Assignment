"""
Question 1 - Testing and Debugging

Write pytest test cases for
a function that adds
two numbers.
"""

from add_numbers import add_numbers


def test_positive_numbers() -> None:
    """
    Verify addition of positive numbers.
    """

    assert add_numbers(5, 3) == 8


def test_negative_numbers() -> None:
    """
    Verify addition of negative numbers.
    """

    assert add_numbers(-5, -3) == -8


def test_zero() -> None:
    """
    Verify addition with zero.
    """

    assert add_numbers(5, 0) == 5


def test_mixed_numbers() -> None:
    """
    Verify addition of
    positive and negative numbers.
    """

    assert add_numbers(10, -5) == 5