"""
Question 4 - Exception Handling

Handle multiple exceptions in a single program.
"""

from pathlib import Path


def get_student_mark(
        file_name: str,
        index: int
) -> str:
    """
    Read student marks from a file and
    return the mark at the specified index.
    """

    file = None

    try:
        # Locate the file relative to the
        # current script location.
        file_path = Path(__file__).parent / file_name

        file = open(
            file_path,
            "r",
            encoding="utf-8"
        )

        marks = file.read().splitlines()

        # Accessing an invalid index may
        # raise IndexError.
        mark = float(marks[index])

    # Handling different exception types
    # prevents the program from terminating
    # unexpectedly and provides clear feedback.
    except FileNotFoundError:
        return "File not found."

    except IndexError:
        return "Index out of range."

    except ValueError:
        return (
            "Invalid numeric value "
            "found in the file."
        )

    else:
        return f"Student Mark: {mark}"

    finally:
        # Closing the file ensures proper
        # resource cleanup.
        if file is not None:
            file.close()


if __name__ == "__main__":

    print("\n--- Multiple Exception Handling ---")

    file_name = input("Enter file name: ")

    index = int(
        input("Enter index: ")
    )

    print(
        get_student_mark(
            file_name,
            index
        )
    )