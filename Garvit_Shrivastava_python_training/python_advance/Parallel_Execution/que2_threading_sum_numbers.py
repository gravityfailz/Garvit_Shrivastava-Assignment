"""
Question 2 - Parallel Execution

Create a thread that
calculates the sum of
numbers from 1 to 100.
"""

import threading

START_NUMBER = 1
END_NUMBER = 100


def calculate_sum() -> None:
    """
    Calculate and display
    the sum of numbers.
    """

    # Ensure a valid range.
    if START_NUMBER > END_NUMBER:
        print("Invalid range.")
        return

    total = sum(
        range(START_NUMBER, END_NUMBER + 1)
    )

    print(f"Sum: {total}")


if __name__ == "__main__":

    # Create and start
    # the worker thread.
    sum_thread = threading.Thread(
        target=calculate_sum
    )

    sum_thread.start()

    # Wait for thread completion.
    sum_thread.join()