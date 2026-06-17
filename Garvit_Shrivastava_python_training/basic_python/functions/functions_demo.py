"""
Question 16
"""


def is_prime(number: int) -> bool:
    """Check whether a number is prime."""

    if number <= 1:
        return False

    for divisor in range(2, int(number ** 0.5) + 1):
        if number % divisor == 0:
            return False

    return True


if __name__ == "__main__":
    print(is_prime(17))

"""
Question 17
"""


def calculate_square(number: float) -> float:
    """Return square of a number."""

    return number * number


if __name__ == "__main__":
    print(calculate_square(8))


"""
Question 18
"""


def is_palindrome(value: str) -> bool:
    """Check whether value is palindrome."""

    processed_value: str = str(value)

    return (
        processed_value
        == processed_value[::-1]
    )


if __name__ == "__main__":
    print(is_palindrome("madam"))
    print(is_palindrome("121"))




"""
Question 19
"""


def find_maximum_number(
    numbers: list[int]
) -> int:
    """Return maximum number."""

    return max(numbers)


if __name__ == "__main__":
    print(
        find_maximum_number(
            [10, 25, 65, 11, 2]
        )
    )