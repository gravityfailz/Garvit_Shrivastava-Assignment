"""
Question 35
"""

FILE_NAME: str = "student.txt"


def write_name() -> None:
    """Write name to file."""

    with open(
        FILE_NAME,
        "w",
        encoding="utf-8"
    ) as file:
        file.write("Garvit Shrivastava")


if __name__ == "__main__":
    write_name()