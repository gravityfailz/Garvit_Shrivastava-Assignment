"""
Question 4 - Functional Programming
Use reduce() to find the
product of all elements in a list.
"""

from functools import reduce

def get_product(numbers: list[int]) -> int:
    """
    Return the product of all
    elements using reduce().
    """

    # An empty list cannot produce
    # a meaningful product value.
    if not numbers:
        raise ValueError(
            "The list cannot be empty."
        )

    # reduce() combines all values
    # into a single result.
    return reduce(
        lambda first, second: first * second,
        numbers
    )


if __name__ == "__main__":

    print("\n--- Reduce Example ---")

    numbers = [1, 2, 3, 4, 5]

    # Display the final product of all elements in a list.
    print(get_product(numbers))