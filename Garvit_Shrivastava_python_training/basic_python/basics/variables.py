"""
Question 4
"""


def display_data_types() -> None:
    """Display variable types."""

    integer_value: int = 10
    float_value: float = 15.5
    string_value: str = "Python"
    boolean_value: bool = True

    print(type(integer_value))
    print(type(float_value))
    print(type(string_value))
    print(type(boolean_value))


if __name__ == "__main__":
    display_data_types()


"""
Question 5
"""


def swap_numbers(
    first_number: int,
    second_number: int
) -> tuple[int, int]:
    """Swap two numbers."""

    return second_number, first_number


if __name__ == "__main__":
    number_one: int = 10
    number_two: int = 20

    number_one, number_two = swap_numbers(
        number_one,
        number_two
    )

    print(number_one, number_two)

"""
Question 6
"""


def calculate_operations(
    first_number: float,
    second_number: float
) -> None:
    """Perform arithmetic operations."""

    print("Sum:", first_number + second_number)
    print("Difference:", first_number - second_number)
    print("Multiplication:", first_number * second_number)
    print("Division:", first_number / second_number)


if __name__ == "__main__":
    calculate_operations(20, 10)