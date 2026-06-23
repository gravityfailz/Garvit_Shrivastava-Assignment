"""
Question 5 - Exception Handling

Write a program that catches all exceptions
and prints the error message.
"""


def get_list_value(
        values: list[int],
        index: int
) -> int:
    """
    Return the value at the specified index.
    """

    return values[index]


def get_value_message(
        values: list[int],
        index_input: str
) -> str:
    """
    Return a success or error message.
    """

    try:
        # Convert the entered index into an integer.
        index = int(index_input)

        value = get_list_value(
            values,
            index
        )

    except Exception as error:
        # Show the error if something goes wrong.
        return f"Error: {error}"

    return f"Value at index {index}: {value}"


if __name__ == "__main__":

    print("\n--- Catch All Exceptions ---")

    numbers = [1, 2, 3, 0, 5]

    index = input("Enter an index: ")

    print(
        get_value_message(
            numbers,
            index
        )
    )