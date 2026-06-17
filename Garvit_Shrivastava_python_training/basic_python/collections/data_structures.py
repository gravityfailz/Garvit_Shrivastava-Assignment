"""
Question 25
"""


def perform_list_operations() -> None:
    """List operations."""

    numbers: list[int] = [
        10, 20, 30, 10, 50,
        60, 20, 70, 80, 90
    ]

    print("Sum:", sum(numbers))
    print("Max:", max(numbers))
    print("Sorted:", sorted(numbers))
    print(
        "Without Duplicates:",
        list(set(numbers))
    )


if __name__ == "__main__":
    perform_list_operations()


"""
Question 26
"""


def count_even_odd(
    numbers: list[int]
) -> tuple[int, int]:
    """Count even and odd numbers."""

    even_count: int = 0
    odd_count: int = 0

    for number in numbers:
        if number % 2 == 0:
            even_count += 1
        else:
            odd_count += 1

    return even_count, odd_count


if __name__ == "__main__":
    print(
        count_even_odd(
            [1, 2, 3, 4, 5, 6]
        )
    )

"""
Question 27
"""


def reverse_list(
    values: list[int]
) -> list[int]:
    """Reverse list."""

    return values[::-1]


if __name__ == "__main__":
    print(
        reverse_list(
            [1, 2, 3, 4, 5]
        )
    )


"""
Question 28
"""


def tuple_example() -> None:
    """Access tuple elements."""

    student_data: tuple = (
        101,
        "Garvit",
        "Bhopal"
    )

    print(student_data[0])
    print(student_data[1])
    print(student_data[2])


if __name__ == "__main__":
    tuple_example()


"""
Question 29
"""


def modify_tuple() -> list:
    """Convert tuple to list."""

    subjects: tuple = (
        "Python",
        "Java",
        "SQL"
    )

    subject_list: list = list(
        subjects
    )

    subject_list.append(
        "MongoDB"
    )

    return subject_list


if __name__ == "__main__":
    print(modify_tuple())

"""
Question 30
"""


def set_operations() -> None:
    """Perform set operations."""

    first_set: set[int] = {
        1, 2, 3, 4, 5
    }

    second_set: set[int] = {
        4, 5, 6, 7, 8
    }

    print(
        "Union:",
        first_set.union(second_set)
    )

    print(
        "Intersection:",
        first_set.intersection(
            second_set
        )
    )

    print(
        "Difference:",
        first_set.difference(
            second_set
        )
    )


if __name__ == "__main__":
    set_operations()


"""
Question 31
"""


def remove_duplicates(
    numbers: list[int]
) -> list[int]:
    """Remove duplicates from list."""

    return list(set(numbers))


if __name__ == "__main__":
    print(
        remove_duplicates(
            [1, 2, 2, 3, 4, 4, 5]
        )
    )

"""
Question 32
"""


def display_student_details() -> None:
    """Display dictionary values."""

    student: dict[str, object] = {
        "id": 101,
        "name": "Garvit",
        "course": "CSE AIML"
    }

    print(student["id"])
    print(student["name"])
    print(student["course"])


if __name__ == "__main__":
    display_student_details()

"""
Question 33
"""


def character_frequency(
    text: str
) -> dict[str, int]:
    """Count character frequency."""

    frequency: dict[str, int] = {}

    for character in text:
        frequency[character] = (
            frequency.get(character, 0) + 1
        )

    return frequency


if __name__ == "__main__":
    print(
        character_frequency(
            "python"
        )
    )