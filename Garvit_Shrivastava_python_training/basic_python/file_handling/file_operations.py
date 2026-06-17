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


"""
Question 37
"""

FILE_NAME: str = "student.txt"


def append_data() -> None:
    """Append data to file."""

    with open(
        FILE_NAME,
        "a",
        encoding="utf-8"
    ) as file:
        file.write(
            "\nPython Training"
        )


if __name__ == "__main__":
    append_data()

"""
Question 38
"""

SOURCE_FILE: str = "student.txt"
TARGET_FILE: str = "copy.txt"


def copy_file_content() -> None:
    """Copy file content."""

    with open(
        SOURCE_FILE,
        "r",
        encoding="utf-8"
    ) as source:
        content: str = source.read()

    with open(
        TARGET_FILE,
        "w",
        encoding="utf-8"
    ) as target:
        target.write(content)


if __name__ == "__main__":
    copy_file_content()

"""
Question 39
"""

FILE_NAME: str = "student.txt"


def search_word(
    word: str
) -> bool:
    """Search word in file."""

    with open(
        FILE_NAME,
        "r",
        encoding="utf-8"
    ) as file:
        content: str = file.read()

    return word in content


if __name__ == "__main__":
    print(
        search_word(
            "Python"
        )
    )