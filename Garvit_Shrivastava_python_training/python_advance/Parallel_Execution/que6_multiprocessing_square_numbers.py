"""
Question 6 - Parallel Execution

Write a multiprocessing
program to calculate the
square of numbers using
Process class.

Multiprocessing:
It allows multiple processes
to run independently and
perform tasks concurrently.
"""

import multiprocessing


def calculate_square(number: int) -> None:
    """
    Calculate and display
    the square of a number.
    """

    print(
        f"Square of {number}: "
        f"{number ** 2}"
    )


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

        processes = []

        for number in numbers:

            process = multiprocessing.Process(
                target=calculate_square,
                args=(number,)
            )

            processes.append(process)

            process.start()

        for process in processes:
            process.join()