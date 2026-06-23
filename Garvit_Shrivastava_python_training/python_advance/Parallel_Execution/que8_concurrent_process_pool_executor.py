"""
Question 8 - Parallel Execution

Convert a normal function
into parallel execution
using ProcessPoolExecutor.

ProcessPoolExecutor:
It manages a pool of processes
and executes tasks concurrently,
utilizing multiple CPU cores.
"""

from concurrent.futures import ProcessPoolExecutor


def calculate_cube(number: int) -> int:
    """
    Return the cube
    of a number.
    """

    return number ** 3


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

        with ProcessPoolExecutor() as executor:

            results = executor.map(
                calculate_cube,
                numbers
            )

        print("Cubes:")

        for result in results:
            print(result)