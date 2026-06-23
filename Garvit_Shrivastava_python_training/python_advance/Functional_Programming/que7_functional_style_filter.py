"""
Question 7 - Functional Programming

Convert a simple loop-based program
into a functional style using filter().
"""


def get_passing_marks(marks: list[int]) -> list[int]:
    """
    Return marks greater than
    or equal to 40.
    """

    # Traditional loop approach:
    # passing_marks = []
    # for mark in marks:
    #     if mark >= 40:
    #         passing_marks.append(mark)

    # filter() replaces the loop and keeps only matching values.
    return list(filter(lambda mark: mark >= 40, marks))


if __name__ == "__main__":

    print("\n--- Functional Style Example ---")

    marks = [25, 40, 55, 32, 78, 90]

    # Display only students who passes the creteria
    print(get_passing_marks(marks))