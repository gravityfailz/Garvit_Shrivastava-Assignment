"""
Question 12
"""


def print_numbers() -> None:
    """Print numbers from 1 to 100."""

    for number in range(1, 101):
        print(number)


if __name__ == "__main__":
    print_numbers()

"""
Question 13
"""


def print_multiplication_table(number: int) -> None:
    """Print multiplication table."""

    for multiplier in range(1, 11):
        print(
            f"{number} x {multiplier} = "
            f"{number * multiplier}"
        )


if __name__ == "__main__":
    print_multiplication_table(5)

"""
Question 14
"""


def calculate_factorial(number: int) -> int:
    """Calculate factorial."""

    factorial_result: int = 1

    for value in range(1, number + 1):
        factorial_result *= value

    return factorial_result


if __name__ == "__main__":
    print(calculate_factorial(5))