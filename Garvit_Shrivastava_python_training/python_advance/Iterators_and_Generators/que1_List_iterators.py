"""
Question 1 - Iterators and Generators

Create an iterator for a list and
print elements using next().
"""


def print_list_elements(
        values: list[int]
) -> None:
    """
    Print list elements using
    an iterator and next().
    """

    # iter() creates an iterator object from the given list.
    iterator = iter(values)

    try:
        while True:
            # next() returns one element at a time from the iterator.

            print(next(iterator))

    except StopIteration:
        # Raised automatically when no elements are left.
        print("\nIteration completed.")


if __name__ == "__main__":

    print("\n--- List Iterator Example ---")

    numbers = [1, 2, 3, 4, 5]

    print_list_elements(numbers)