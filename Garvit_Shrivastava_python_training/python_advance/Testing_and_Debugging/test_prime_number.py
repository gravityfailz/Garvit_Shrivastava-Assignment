"""
Question 2 - Testing and Debugging
Write pytest test cases for
a function that checks
whether a number is prime.
"""

from prime_number import is_prime


def test_prime_number() -> None:
    """
    Verify a prime number.
    """

    assert is_prime(7)


def test_non_prime_number() -> None:
    """
    Verify a non-prime number.
    """

    assert not is_prime(8)


def test_smallest_prime() -> None:
    """
    Verify the smallest
    prime number.
    """

    assert is_prime(2)


def test_zero() -> None:
    """
    Verify zero.
    """

    assert not is_prime(0)


def test_one() -> None:
    """
    Verify one.
    """

    assert not is_prime(1)


def test_negative_number() -> None:
    """
    Verify a negative number.
    """

    assert not is_prime(-5)