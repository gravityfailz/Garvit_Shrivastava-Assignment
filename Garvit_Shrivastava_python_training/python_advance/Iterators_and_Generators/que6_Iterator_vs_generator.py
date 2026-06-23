
"""
Question 6
Difference Between Iterator and Generator

Iterator:
- An iterator is used to access elements
  one by one from a collection.
- It works with iter() and next().
- When no elements are left,
  StopIteration is raised.

Generator:
- A generator is a function that uses
  the yield keyword.
- It returns values one at a time.
- It is useful when working with
  large amounts of data.
"""


def demonstrate_iterator() -> None:
    """
    Show an iterator example.
    """

    numbers = [1, 2, 3]

    #  iter() Create an iterator from the list.
    iterator = iter(numbers)

    print("Iterator Output:")

    print(next(iterator))
    print(next(iterator))
    print(next(iterator))


def demonstrate_generator():
    """
    Show a generator example.
    """

    # Return values one by one.
    yield 1
    yield 2
    yield 3


if __name__ == "__main__":

    print("\n--- Iterator vs Generator ---\n")

    demonstrate_iterator()

    print("\nGenerator Output:")

    for value in demonstrate_generator():
        print(value)

