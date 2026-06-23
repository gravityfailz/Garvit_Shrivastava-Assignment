"""
Question 3
Write a generator function that
yields square numbers up to N.
"""


def generate_squares(
        limit: int
):
    """
    Generate square numbers
    from 1 to N.
    """

    for number in range(1, limit + 1):

        # it returns one value at a time without storing all values in memory.
        yield number ** 2


if __name__ == "__main__":

    print("\n--- Square Number Generator ---")

    limit = int(input("Enter N: "))

    if limit < 1:
        print("Please enter a positive number.")
    else:
        for square in generate_squares(limit):
            print(square)