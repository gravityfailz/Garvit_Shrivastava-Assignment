"""
Question 7 - Parallel Execution

Convert a normal function
into parallel execution
using ThreadPoolExecutor.

ThreadPoolExecutor:
It manages a pool of threads
and executes tasks concurrently,
reducing manual thread management.
"""

from concurrent.futures import ThreadPoolExecutor


def calculate_square(number: int) -> int:
    """
    Return the square
    of a number.
    """

    return number ** 2


if __name__ == "__main__":

    user_input = input(
        "Enter numbers separated by spaces: "
    )

    numbers = [
        int(number)
        for number in user_input.split()
    ]

    if not numbers:
        print("No numbers available.")
    else:

        with ThreadPoolExecutor() as executor:

            results = executor.map(
                calculate_square,
                numbers
            )

        print("Squares:")

        for result in results:
            print(result)