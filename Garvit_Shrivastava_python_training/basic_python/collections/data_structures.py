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