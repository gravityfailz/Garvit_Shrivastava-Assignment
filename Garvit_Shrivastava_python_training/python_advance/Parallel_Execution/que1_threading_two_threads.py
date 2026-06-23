"""
Question 1 - Parallel Execution

Write a program to create
two threads that print
numbers from 1 to 5
simultaneously.
"""

import threading


def print_numbers(thread_name: str) -> None:
    """
    Print numbers from 1 to 5.
    """

    for number in range(1, 6):
        print(f"{thread_name}: {number}")


if __name__ == "__main__":

    # Create threads to execute
    # the same function concurrently.
    first_thread = threading.Thread(
        target=print_numbers,
        args=("Thread 1",)
    )

    second_thread = threading.Thread(
        target=print_numbers,
        args=("Thread 2",)
    )

    # Start thread execution.
    first_thread.start()
    second_thread.start()

    # Wait for both threads
    # to complete execution.
    first_thread.join()
    second_thread.join()