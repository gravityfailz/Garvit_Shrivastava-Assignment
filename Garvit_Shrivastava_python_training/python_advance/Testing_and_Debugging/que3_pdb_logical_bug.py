"""
Question 3 - Testing and Debugging

Create a function with a logical bug
and use pdb to identify the issue.
"""

import pdb


def calculate_average(total_marks: int, subject_count: int) -> float:
    """
    Return the average marks.
    """

    # Start debugger
    pdb.set_trace()

    # Logical bug: multiplication is used
    # instead of division.
    average = total_marks * subject_count

    return average


if __name__ == "__main__":
    result = calculate_average(500, 5)
    print(f"Average Marks: {result}")