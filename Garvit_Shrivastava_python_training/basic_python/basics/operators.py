"""
Question 7
"""


def check_even_or_odd(number: int) -> str:
    """Check whether number is even or odd."""

    return "Even" if number % 2 == 0 else "Odd"


if __name__ == "__main__":
    print(check_even_or_odd(12))