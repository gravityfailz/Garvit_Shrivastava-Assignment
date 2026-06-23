"""
Question 6 - Functional Programming

Write a recursive function
to calculate Fibonacci.
"""


def calculate_fibonacci(number: int) -> int:
    """
    Return the Fibonacci value
    using recursion.
    """

    # First two Fibonacci numbers are 0 and 1.
    if number <= 1:
        return number

    # Recursive call calculates the previous two Fibonacci values.
    return (
            calculate_fibonacci(number - 1)
            + calculate_fibonacci(number - 2)
    )


if __name__ == "__main__":

    print("\n--- Recursive Fibonacci ---")

    number = int(input("Enter a position: "))

    if number < 0:
        print("Please enter a non-negative number.")
    else:

        # Display the Fibonacci value for the position asked.
        print(calculate_fibonacci(number))