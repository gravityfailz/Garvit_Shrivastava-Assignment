"""
Question 22
"""

import math


def math_operations() -> None:
    """Perform math operations."""

    print(math.sqrt(25))
    print(math.pow(2, 5))
    print(math.factorial(5))


if __name__ == "__main__":
    math_operations()

"""
Question 23
"""

import random


def generate_random_numbers() -> None:
    """Generate random values."""

    print(
        random.randint(1, 100)
    )

    print(
        random.uniform(1, 10)
    )


if __name__ == "__main__":
    generate_random_numbers()

"""
Question 24
"""

from custom_module import (
    add_numbers
)


def demonstrate_custom_module() -> None:
    """Use custom module."""

    print(
        add_numbers(10, 20)
    )


if __name__ == "__main__":
    demonstrate_custom_module()