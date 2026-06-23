"""
Question 5 - Functional Programming

Write a recursive function
to calculate factorial.
"""


def calculate_factorial(number: int) -> int:
    """
    Return the factorial
    using recursion.
    """

    # Factorial of 0 and 1 is 1.
    if number <= 1:
        return 1

    # Recursive call brakes the problem into smaller sub problems.
    # the problem gets brake down into smaller once until the base condition is met.
    return number * calculate_factorial(number - 1)


if __name__ == "__main__":

    print("\n--- Recursive Factorial ---")

    number = int(input("Enter a number: "))

    if number < 0:
        print("Please enter a non-negative number.")
    else:

        # Display the factorial calculated using recursion.
        print(calculate_factorial(number))