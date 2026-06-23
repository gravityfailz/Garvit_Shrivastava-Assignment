"""
Question 4 - Parallel Execution

Create multiple threads to
simulate file downloading
using time.sleep().

Each thread represents
a file download task.
"""

import threading
import time


def download_file(file_name: str) -> None:
    """
    Simulate file download.
    """

    print(f"Downloading {file_name}...")

    # Simulate download time.
    time.sleep(2)

    print(f"{file_name} downloaded.")


if __name__ == "__main__":

    file_names = [
        "File1.pdf",
        "File2.pdf",
        "File3.pdf"
    ]

    threads = []

    for file_name in file_names:

        # Create a thread for
        # each download task.
        thread = threading.Thread(
            target=download_file,
            args=(file_name,)
        )

        threads.append(thread)

        # Start thread execution.
        thread.start()

    # Wait for all downloads to complete.
    for thread in threads:
        thread.join()