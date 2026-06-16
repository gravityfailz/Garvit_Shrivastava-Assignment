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


"""
Question 9
"""


def find_largest_number(
    first_number: int,
    second_number: int,
    third_number: int
) -> int:
    """Return largest number."""

    return max(
        first_number,
        second_number,
        third_number
    )


if __name__ == "__main__":
    print(find_largest_number(10, 25, 15))

"""
Question 10
"""

GRADE_A_MARKS: int = 90
GRADE_B_MARKS: int = 75
GRADE_C_MARKS: int = 50


def calculate_grade(marks: int) -> str:
    """Calculate grade."""

    if marks >= GRADE_A_MARKS:
        return "A"

    if marks >= GRADE_B_MARKS:
        return "B"

    if marks >= GRADE_C_MARKS:
        return "C"

    return "Fail"


if __name__ == "__main__":
    print(calculate_grade(82))

"""
Question 11
"""


def is_leap_year(year: int) -> bool:
    """Check leap year."""

    return (
        year % 400 == 0
        or (
            year % 4 == 0
            and year % 100 != 0
        )
    )


if __name__ == "__main__":
    print(is_leap_year(2024))