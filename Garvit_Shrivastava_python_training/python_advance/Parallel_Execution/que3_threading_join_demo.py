"""
Question 3 - Parallel Execution

Demonstrate the use of
join() method in threading.

The join() method makes
the main program wait
until a thread completes
its execution.
"""

import threading
import time


def perform_task() -> None:
    """
    Simulate a task using
    a delay.
    """

    print("Task started.")

    # Simulate task execution.
    time.sleep(2)

    print("Task completed.")


if __name__ == "__main__":

    task_thread = threading.Thread(
        target=perform_task
    )

    # Start thread execution.
    task_thread.start()

    # Wait for the thread
    # to finish execution.
    task_thread.join()

    print("Main program completed.")