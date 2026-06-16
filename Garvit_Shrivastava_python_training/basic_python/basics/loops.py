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