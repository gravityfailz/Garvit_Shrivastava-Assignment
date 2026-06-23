"""
Question 2 - Testing and Debugging

Create a function that
checks whether a number
is prime.
"""


def is_prime(number: int) -> bool:
    """
    Return True if the
    number is prime.
    """

    # Numbers less than 2
    # are not prime.
    if number < 2:
        return False

    # Check divisibility by
    # all numbers before itself.
    for divisor in range(2, number):

        if number % divisor == 0:
            return False

    return True