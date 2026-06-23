"""
Question 1 - Exception Handling

Write a program that takes a number as input and
handles ValueError if the input is not a valid integer.
"""


def convert_to_integer(value: str) -> int:
    """
    Convert the provided string value into an integer.

    Args:
        value: User provided input.

    Returns:
        Converted integer value.

    Raises:
        ValueError:
            If the input cannot be converted into an integer.
    """

    return int(value)


def get_integer_message(value: str) -> str:
    """
    Return a success or error message
    based on the provided input.
    """

    try:
        # Separate conversion logic improves
        # reusability and testability.
        number = convert_to_integer(value)

    except ValueError:
        return (
            "Invalid input. "
            "Please enter a valid integer."
        )

    return f"Valid Integer: {number}"


if __name__ == "__main__":

    print("\n--- Integer Input Validation ---")

    user_input = input("Enter an integer: ")

    print(get_integer_message(user_input))