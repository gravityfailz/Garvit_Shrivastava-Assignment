"""
Question 7
"""


def check_even_or_odd(number: int) -> str:
    """Check whether number is even or odd."""

    return "Even" if number % 2 == 0 else "Odd"


if __name__ == "__main__":
    print(check_even_or_odd(12))


"""
Question 8
"""


def identify_number_type(number: int) -> str:
    """Identify number type."""

    if number > 0:
        return "Positive"

    if number < 0:
        return "Negative"

    return "Zero"


if __name__ == "__main__":
    print(identify_number_type(-5))