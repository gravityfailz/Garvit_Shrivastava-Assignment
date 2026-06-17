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

"""
Question 36
"""

FILE_NAME: str = "student.txt"


def count_file_statistics() -> None:
    """Count file statistics."""

    with open(
        FILE_NAME,
        "r",
        encoding="utf-8"
    ) as file:
        content: str = file.read()

    words: int = len(content.split())
    lines: int = len(content.splitlines())
    characters: int = len(content)

    print("Words:", words)
    print("Lines:", lines)
    print("Characters:", characters)


if __name__ == "__main__":
    count_file_statistics()