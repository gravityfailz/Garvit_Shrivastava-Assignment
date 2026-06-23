"""
Question 4 - Testing and Debugging

Use pdb breakpoints inside
a loop and inspect
variable values.
"""

import pdb


def calculate_total() -> None:
    """
    Calculate the running total
    of numbers in a list.
    """

    numbers = [10, 20, 30, 40]
    total = 0

    for number in numbers:

        # Pause execution to inspect
        # current values in each iteration.
        pdb.set_trace()

        # Update running total
        # during each iteration.
        total += number

    print(f"Total: {total}")


if __name__ == "__main__":
    calculate_total()