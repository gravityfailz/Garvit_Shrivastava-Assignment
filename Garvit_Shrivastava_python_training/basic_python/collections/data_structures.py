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