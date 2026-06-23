
"""
Question 4 - Iterators and Generators

Write a generator to produce
Fibonacci numbers.
"""


def generate_fibonacci(
        limit: int
):
    """
    Generate Fibonacci numbers
    up to the specified count.
    """

    first_number = 0
    second_number = 1

    for _ in range(limit):

        # Return the current Fibonacci number.
        yield first_number

        # Calculate the next two numbers.
        first_number, second_number = (
            second_number,
            first_number + second_number
        )


if __name__ == "__main__":

    print("\n--- Fibonacci Generator ---")

    limit = int(input("Enter count: "))

    if limit < 1:
        print("Please enter a positive number.")
    else:
        for number in generate_fibonacci(limit):
            print(number)
