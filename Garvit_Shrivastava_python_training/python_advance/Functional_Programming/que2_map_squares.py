"""
Question 2 - Functional Programming

Use map() to convert a list
of numbers into their squares.
"""


def get_squared_numbers(numbers: list[int]) -> list[int]:
    """
    Return square values
    using map().
    """

    # map() applies the square operation to each and every element.
    return list(map(lambda number: number ** 2, numbers))


if __name__ == "__main__":

    print("\n--- Map Example ---")

    numbers = [1, 2, 3, 4, 5]

    # Display squared values that gets generated using map().
    print(get_squared_numbers(numbers))